import asyncio
import aio_pika
import logging
import uuid
import json
from .config import establish_rabbitmq_connection
from .publisher import send_order_request
from .consumer import handle_order_response, handle_response
from .publisher import send_message_to_service

async def fetch_customer_orders(customer_id: int):
    """Fetch orders for a given customer ID by communicating with the Order service via RabbitMQ."""
    try:
        # Establish connection to RabbitMQ
        connection = await establish_rabbitmq_connection()
        async with connection:
            channel = await connection.channel()

            result_queue = await channel.declare_queue('', exclusive=True, auto_delete=True)
            callback_queue = result_queue.name
            logging.info(f"Temporary callback queue declared: {callback_queue}")
            response_future = asyncio.Future()
            correlation_id = str(uuid.uuid4())

            await result_queue.consume(lambda message: handle_order_response(message, response_future, correlation_id))
            await send_order_request(channel, customer_id, callback_queue, correlation_id)

            try:
                orders_data = await asyncio.wait_for(response_future, timeout=10)
                return orders_data

            except asyncio.TimeoutError:
                logging.error(f"Timeout while waiting for order service response for customer {customer_id}")
                raise TimeoutError("Request to order service timed out")

    except Exception as e:
        logging.error(f"Error in fetching customer orders: {str(e)}")
        raise

    finally:
        if connection and not connection.is_closed:
            await connection.close()
            logging.info("RabbitMQ connection closed.")

async def fetch_order_products(customer_id: int, order_id: int):
    """Fetch products for a given customer order by communicating with the Order and Product services."""
    try:
        order_service_response = await fetch_order_details(customer_id, order_id)
        print(f"Order service response: {order_service_response}")
        
        product_ids = order_service_response.get('products', [])
        print(f"product IDs: {product_ids}")
        if not isinstance(product_ids, list):
            raise ValueError(f"Expected a list of product IDs, got {type(product_ids)}")

        product_details = await fetch_product_details(product_ids)
        print(f"product details from service: {product_details}")

        return product_details

    except Exception as e:
        logging.error(f"Error in fetching order products for customer {customer_id}, order {order_id}: {str(e)}")
        raise

async def fetch_order_details(customer_id: int, order_id: int):
    """Fetch product IDs from the Order service."""
    try:
        connection = await establish_rabbitmq_connection()
        async with connection:
            channel = await connection.channel()
            result_queue = await channel.declare_queue('', exclusive=True, auto_delete=True)
            correlation_id = str(uuid.uuid4())
            response_future = asyncio.Future()

            await result_queue.consume(lambda message: handle_response(message, response_future, correlation_id, 'products'))

            await send_message_to_service(
                channel=channel,
                routing_key='order.products.request',
                message={'order_id': order_id},
                reply_to=result_queue.name,
                correlation_id=correlation_id
            )

            try:
                product_ids = await asyncio.wait_for(response_future, timeout=10)
                logging.info(f"Product IDs received: {product_ids}")

                if isinstance(product_ids, list):
                    return {'products': product_ids}
                else:
                    raise ValueError("Unexpected response format from order service")

            except asyncio.TimeoutError:
                logging.error(f"Timeout while waiting for order service response for order {order_id}")
                raise TimeoutError("Request to order service timed out")

    except Exception as e:
        logging.error(f"Error in fetching order details: {str(e)}")
        raise

async def fetch_product_details(product_ids: list):
    """Fetch product details from the Product service."""
    connection = await establish_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()
        result_queue = await channel.declare_queue('', exclusive=True, auto_delete=True)
        correlation_id = str(uuid.uuid4())
        response_future = asyncio.Future()

        await result_queue.consume(lambda message: handle_response(message, response_future, correlation_id, 'list'))
        await send_message_to_service(
            channel=channel,
            routing_key='product_details_queue',
            message={'product_ids': product_ids},
            reply_to=result_queue.name,
            correlation_id=correlation_id
        )

        try:
            product_details = await asyncio.wait_for(response_future, timeout=10)

            if isinstance(product_details, list):
                return product_details  
            else:
                logging.error(f"Unexpected response format: {product_details}")
                return [] 

        except asyncio.TimeoutError:
            logging.error(f"Timeout waiting for Product Service response for product IDs {product_ids}")
            raise TimeoutError("Product Service request timed out.")
        


async def process_notification_message(message: aio_pika.IncomingMessage):
    async with message.process():
        notification_data = json.loads(message.body)
        
        print(f"Sending notification to customer {notification_data['customer_id']}: {notification_data['message']}")


async def start_notification_consumer():
    connection = await aio_pika.connect_robust("amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.get_queue('notifications')
        await queue.consume(process_notification_message)
        print("Notification consumer started. Waiting for messages...")
        await asyncio.Future()
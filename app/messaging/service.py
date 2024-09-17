import asyncio
import aio_pika
import logging
import uuid
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

            # Declare a temporary queue to receive the response
            result_queue = await channel.declare_queue('', exclusive=True, auto_delete=True)
            callback_queue = result_queue.name
            logging.info(f"Temporary callback queue declared: {callback_queue}")

            # Initialize the response future
            response_future = asyncio.Future()

            # Define the correlation ID to track responses
            correlation_id = str(uuid.uuid4())

            # Set up the consumer for the callback queue
            await result_queue.consume(lambda message: handle_order_response(message, response_future, correlation_id))

            # Send the request to the Order service
            await send_order_request(channel, customer_id, callback_queue, correlation_id)

            # Wait for the response with a timeout
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
        # Step 1: Fetch product IDs from the Order service
        order_service_response = await fetch_order_details(customer_id, order_id)
        print(f"Order service response: {order_service_response}")
        
        # Here, ensure you're handling the product IDs correctly
        product_ids = order_service_response.get('products', [])
        print(f"product IDs: {product_ids}")
        if not isinstance(product_ids, list):
            raise ValueError(f"Expected a list of product IDs, got {type(product_ids)}")

        # Step 2: Fetch product details from the Product service
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

            # Subscribe to the callback queue
            await result_queue.consume(lambda message: handle_response(message, response_future, correlation_id, 'products'))

            # Send request to Order service
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
                    return {'products': product_ids}  # Return products in expected format
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

        # Consume response from the Product Service
        await result_queue.consume(lambda message: handle_response(message, response_future, correlation_id, 'list'))

        # Send request to Product Service
        await send_message_to_service(
            channel=channel,
            routing_key='product_details_queue',
            message={'product_ids': product_ids},
            reply_to=result_queue.name,
            correlation_id=correlation_id
        )

        try:
            product_details = await asyncio.wait_for(response_future, timeout=10)

            # Check if the response is a list (which it should be)
            if isinstance(product_details, list):
                return product_details  # Return the list of product details
            else:
                logging.error(f"Unexpected response format: {product_details}")
                return []  # Return an empty list if the format is unexpected

        except asyncio.TimeoutError:
            logging.error(f"Timeout waiting for Product Service response for product IDs {product_ids}")
            raise TimeoutError("Product Service request timed out.")
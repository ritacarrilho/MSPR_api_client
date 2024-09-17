import asyncio
import aio_pika
import logging
import uuid
from .config import establish_rabbitmq_connection
from .publisher import send_order_request
from .consumer import handle_order_response

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
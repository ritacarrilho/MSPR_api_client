import logging
import asyncio
import uuid
import json
import aio_pika
import os
from dotenv import load_dotenv

load_dotenv()

BROKER_USER = os.getenv("BROKER_USER")
BROKER_PASSWORD = os.getenv('BROKER_PASSWORD')
BROKER_HOST = os.getenv('BROKER_HOST')
BROKER_PORT = os.getenv('BROKER_PORT')
BROKER_VIRTUAL_HOST = os.getenv('BROKER_VIRTUAL_HOST')

async def fetch_customer_orders(customer_id: int):
    """Fetch orders for a given customer ID by communicating with the Order service via RabbitMQ."""
    try:
        connection = await aio_pika.connect_robust(f"amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}/") 
        async with connection:
            channel = await connection.channel()
            result_queue = await channel.declare_queue('', exclusive=True, auto_delete=True)
            callback_queue = result_queue.name
            correlation_id = str(uuid.uuid4())
            response_future = asyncio.Future()

            async def on_response(message: aio_pika.IncomingMessage):
                if message.correlation_id == correlation_id:
                    response_data = json.loads(message.body)
                    print(response_data)
                    response_future.set_result(response_data['orders'])
                    await message.ack()

            await result_queue.consume(on_response)

            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps({'customer_id': customer_id}).encode(),
                    reply_to=callback_queue,
                    correlation_id=correlation_id,
                ),
                routing_key='customer.orders.request'
            )

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
        if 'connection' in locals() and not connection.is_closed:
            await connection.close()
            logging.info("RabbitMQ connection closed.")
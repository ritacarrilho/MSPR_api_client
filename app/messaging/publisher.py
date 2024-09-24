import aio_pika
import json
import os
import logging

from dotenv import load_dotenv

load_dotenv()

BROKER_USER = os.getenv("BROKER_USER")
BROKER_PASSWORD = os.getenv('BROKER_PASSWORD')
BROKER_HOST = os.getenv('BROKER_HOST')
BROKER_PORT = os.getenv('BROKER_PORT')
BROKER_VIRTUAL_HOST = os.getenv('BROKER_VIRTUAL_HOST')

async def send_order_request(channel, customer_id, callback_queue, correlation_id):
    try:
        message = aio_pika.Message(
            body=json.dumps({'customer_id': customer_id}).encode(),
            reply_to=callback_queue,
            correlation_id=correlation_id,
        )
        await channel.default_exchange.publish(
            message, routing_key='customer.orders.request'
        )
        logging.info(f"Sent order request for customer_id: {customer_id}, correlation_id: {correlation_id}")
    except Exception as e:
        logging.error(f"Failed to send order request: {str(e)}")
        raise


async def send_message_to_service(channel, routing_key, message, reply_to, correlation_id):
    try:
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                reply_to=reply_to,
                correlation_id=correlation_id,
            ),
            routing_key=routing_key
        )
        logging.info(f"Sent message to {routing_key} with correlation_id: {correlation_id}")
    except Exception as e:
        logging.error(f"Failed to send message to {routing_key}: {str(e)}")
        raise


async def publish_notification(customer_id, message_text):
    connection = await aio_pika.connect_robust(f"amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}/")
    async with connection:
        channel = await connection.channel()
        notifications_exchange = await channel.get_exchange('notifications_exchange')
        
        notification_message = aio_pika.Message(
            body=json.dumps({
                "event": "notification_created",
                "customer_id": customer_id,
                "message": message_text,
                "notification_type": "order_confirmation",
                "date_created": "2024-09-24T10:22:00Z"
            }).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        
        await notifications_exchange.publish(notification_message, routing_key='customers.notification')
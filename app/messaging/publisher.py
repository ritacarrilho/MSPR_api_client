import aio_pika
import json
import uuid
import logging

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
import aio_pika
import json
import logging
import asyncio

async def handle_order_response(message, response_future, correlation_id):
    try:
        if message.correlation_id == correlation_id:
            body = message.body.decode('utf-8')
            logging.info(f"Received message: {body}")
            
            try:
                response_data = json.loads(body)
                logging.info(f"Parsed response data: {response_data}")

                if isinstance(response_data, str):
                    # If the response is still a string, parse it again
                    response_data = json.loads(response_data)

                if isinstance(response_data, dict):
                    response_future.set_result(response_data.get('orders', []))
                else:
                    logging.error("Response data is not a dictionary")
                    response_future.set_result([])

            except json.JSONDecodeError as e:
                logging.error(f"Failed to parse JSON: {e}")
                response_future.set_result([])

        await message.ack()
    except Exception as e:
        logging.error(f"Error in processing message: {str(e)}")
        response_future.set_result([])
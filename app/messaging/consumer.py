import aio_pika
import json
import logging
import asyncio

async def handle_order_response(message, response_future, correlation_id):
    try:
        if message.correlation_id == correlation_id:
            body = message.body.decode('utf-8')
            print(f"Received message: {body}")
            
            try:
                response_data = json.loads(body)
                print(f"Parsed response data: {response_data}")

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


async def handle_response(message, response_future, correlation_id, expected_key=None):
    """Handles the incoming response from RabbitMQ."""
    try:
        if message.correlation_id != correlation_id:
            logging.warning("Correlation ID mismatch. Ignoring message.")
            await message.reject(requeue=False)
            return
        
        body = message.body.decode('utf-8')
        logging.info(f"Received raw message body: {body}")

        # Try parsing the response data
        try:
            response_data = json.loads(body)
            logging.info(f"Parsed response data: {response_data}")

            # Handle expected types of responses
            if isinstance(response_data, dict):
                if expected_key and expected_key in response_data:
                    response_future.set_result(response_data[expected_key])
                else:
                    logging.error(f"Key '{expected_key}' not found in response: {response_data}")
                    response_future.set_result([])  # Default to empty list if the key is missing
            elif isinstance(response_data, list):
                # Handle list responses (for products)
                response_future.set_result(response_data)
            else:
                logging.error(f"Unexpected response format: {response_data}")
                response_future.set_result([])

        except json.JSONDecodeError as e:
            logging.error(f"JSON decoding failed: {e}")
            response_future.set_result([])  # Default to empty list on error

        await message.ack()  # Acknowledge the message

    except Exception as e:
        logging.error(f"Error in response callback: {e}")
        response_future.set_result([])  # Default to empty list on unknown error
        await message.reject(requeue=False)
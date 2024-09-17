import aio_pika
import asyncio
import json
import logging
import uuid

async def fetch_customer_orders(customer_id: int):
    """Fetch orders for a given customer ID by communicating with the Order service via RabbitMQ."""
    try:
        # Establish connection to RabbitMQ
        connection = await aio_pika.connect_robust("amqp://user:password@rabbitmq/")
        async with connection:
            channel = await connection.channel()

            # Declare a temporary queue to receive the response
            result_queue = await channel.declare_queue('', exclusive=True, auto_delete=True)
            callback_queue = result_queue.name
            logging.info(f"Temporary callback queue declared: {callback_queue}")

            # Initialize the response future
            response_future = asyncio.Future()  # Define the future that will store the result

            # Define the correlation ID to track responses
            correlation_id = str(uuid.uuid4())

            # Define the callback function for receiving the response
            async def on_response(message: aio_pika.IncomingMessage):
                try:
                    body = message.body.decode('utf-8')
                    logging.info(f"Received raw message body: {body}")

                    # Try parsing the response data
                    try:
                        response_data = json.loads(body)
                        logging.info(f"Parsed response data: {response_data}")

                        if isinstance(response_data, str):
                            # If the response is still a string, parse it again
                            response_data = json.loads(response_data)

                        if isinstance(response_data, dict):
                            # Set the result as the 'orders' field from the response
                            response_future.set_result(response_data.get('orders', []))
                        else:
                            logging.error("Response data is not a dictionary")
                            response_future.set_result([])  # Default to empty list if parsing fails

                    except json.JSONDecodeError as e:
                        logging.error(f"JSON decoding failed: {e}")
                        response_future.set_result([])  # Default to empty list on error

                    await message.ack()  # Acknowledge the message

                except Exception as e:
                    logging.error(f"Error in response callback: {e}")
                    response_future.set_result([])  # Default to empty list on unknown error
                    await message.reject(requeue=False)

            # Subscribe to the callback queue to consume the response
            await result_queue.consume(on_response)

            # Send the request to the Order Service
            logging.info(f"Sending request for customer_id: {customer_id} with correlation_id: {correlation_id}")

            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps({'customer_id': customer_id}).encode(),
                    reply_to=callback_queue,
                    correlation_id=correlation_id,
                ),
                routing_key='customer.orders.request'
            )

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
        if 'connection' in locals() and not connection.is_closed:
            await connection.close()
            logging.info("RabbitMQ connection closed.")
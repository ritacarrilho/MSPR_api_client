import aio_pika
import json
import uuid
import asyncio
import logging

# async def send_rabbitmq_message(customer_id: int):
#     try:
#         logging.info("Connecting to RabbitMQ asynchronously using aio-pika...")
#         connection = await aio_pika.connect_robust("amqp://user:password@rabbitmq/")
#         async with connection:
#             channel = await connection.channel()
#             logging.info("Connected to RabbitMQ asynchronously!")

#             # Declare a temporary queue to receive the response
#             result_queue = await channel.declare_queue('', exclusive=True, auto_delete=True)
#             callback_queue = result_queue.name
#             logging.info(f"Temporary callback queue declared: {callback_queue}")

#             # Ensure the 'customer.orders.request' queue is declared as durable
#             await channel.declare_queue('customer.orders.request', durable=True)

#             # Initialize the response future
#             response_future = asyncio.Future()

#             # Define a callback for receiving the response
#             async def on_response(message: aio_pika.IncomingMessage):
#                 logging.info("Received a message from the callback queue...")
#                 if message.correlation_id == corr_id:
#                     logging.info(f"Correlation ID matched: {corr_id}. Setting the response.")
#                     response_data = json.loads(message.body)
#                     response_future.set_result(response_data['orders'])

#                     # Acknowledge the message to remove it from RabbitMQ
#                     await message.ack()
#                 else:
#                     logging.warning("Correlation ID did not match. Rejecting the message.")
#                     await message.reject(requeue=False)

#             # Subscribe to the callback queue
#             await result_queue.consume(on_response)

#             # Send the request to the Order Service
#             corr_id = str(uuid.uuid4())
#             logging.info(f"Sending request to 'customer.orders.request' with correlation ID: {corr_id}")

#             await channel.default_exchange.publish(
#                 aio_pika.Message(
#                     body=json.dumps({'customer_id': customer_id}).encode(),
#                     reply_to=callback_queue,
#                     correlation_id=corr_id,
#                 ),
#                 routing_key='customer.orders.request'
#             )
#             logging.info(f"Request sent for customer_id: {customer_id}")

#             # Wait for the response (up to a timeout)
#             try:
#                 orders_data = await asyncio.wait_for(response_future, timeout=10)
#                 return orders_data
#             except asyncio.TimeoutError:
#                 logging.error("Request to order service timed out")
#                 raise TimeoutError("Request to order service timed out")

#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#         raise

#     finally:
#         if 'connection' in locals() and not connection.is_closed:
#             await connection.close()
#             logging.info("RabbitMQ connection closed.")
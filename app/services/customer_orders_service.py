import json
import pika
import uuid
import aio_pika
import asyncio
from datetime import datetime
from fastapi import HTTPException 

async def get_customer_orders(customer_id: int):
    try:
        # Define connection parameters for RabbitMQ using aio-pika
        print("Connecting to RabbitMQ asynchronously using aio-pika...")
        connection = await aio_pika.connect_robust("amqp://user:password@rabbitmq/")
        async with connection:
            channel = await connection.channel()

            print("Connected to RabbitMQ asynchronously!")

            # Declare a temporary queue to receive the response
            result_queue = await channel.declare_queue('', exclusive=True, auto_delete=True)
            callback_queue = result_queue.name
            print(f"Temporary callback queue declared: {callback_queue}")

            # Ensure the 'order_queue_test' queue is declared as durable
            await channel.declare_queue('order_queue_test', durable=True)

            # Initialize the response future
            response_future = asyncio.Future()

            # Define a callback for receiving the response
            async def on_response(message: aio_pika.IncomingMessage):
                print("Received a message from the callback queue...")
                if message.correlation_id == corr_id:
                    print(f"Correlation ID matched: {corr_id}. Setting the response.")
                    response_data = json.loads(message.body)
                    response_future.set_result(response_data['orders'])

                    # Acknowledge the message to remove it from RabbitMQ
                    await message.ack()
                else:
                    print("Correlation ID did not match. Rejecting the message.")
                    await message.reject(requeue=False)  # Reject the message if correlation ID doesn't match, don't requeue it.

            # Subscribe to the callback queue
            await result_queue.consume(on_response)

            # Send the request to the Order Service
            corr_id = str(uuid.uuid4())
            print(f"Sending request to order_queue_test with correlation ID: {corr_id}")

            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps({'customer_id': customer_id}).encode(),
                    reply_to=callback_queue,
                    correlation_id=corr_id,
                ),
                routing_key='order_queue_test'
            )
            print(f"Request sent for customer_id: {customer_id}")

            # Wait for the response (up to a timeout)
            try:
                orders_data = await asyncio.wait_for(response_future, timeout=10)
                print(orders_data)
            except asyncio.TimeoutError:

                raise HTTPException(status_code=504, detail="Request to order service timed out")

            print("Response received, returning orders.")
            orders = [
                {
                    'id_order': order['id_order'],
                    'customerId': customer_id,
                    'createdAt': datetime.fromisoformat(order['createdAt']),
                    'updated_at': datetime.fromisoformat(order['updated_at']),
                    'status': order['status']
                }
                for order in orders_data
            ]
            print(orders)
            return orders

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch customer orders")

    finally:
        if 'connection' in locals() and not connection.is_closed:
            await connection.close()
            print("RabbitMQ connection closed.")
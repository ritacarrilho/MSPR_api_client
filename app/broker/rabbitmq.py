import pika
import json

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
channel = connection.channel()

# Define the queues
request_queue = 'customer.order.request.queue'
response_queue = 'customer.order.response.queue'

def publish_order_request(customer_id: int):
    message = json.dumps({"customer_id": customer_id})
    channel.basic_publish(exchange='customer.order.exchange', routing_key='order.request', body=message)

def listen_for_order_response(customer_id: int):
    # Logic to listen to the response queue for the response from the order service
    pass
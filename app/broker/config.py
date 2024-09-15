import pika
import json
import time

def get_rabbitmq_connection():
    credentials = pika.PlainCredentials('user', 'password')
    return pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672, virtual_host='/', credentials=credentials))

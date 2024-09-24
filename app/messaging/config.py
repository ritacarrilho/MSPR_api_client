import pika
import os
import logging
import time
import aio_pika
import asyncio
from dotenv import load_dotenv

load_dotenv()

BROKER_USER = os.getenv("BROKER_USER")
BROKER_PASSWORD = os.getenv('BROKER_PASSWORD')
BROKER_HOST = os.getenv('BROKER_HOST')
BROKER_PORT = os.getenv('BROKER_PORT')
BROKER_VIRTUAL_HOST = os.getenv('BROKER_VIRTUAL_HOST')

RETRY_DELAY = 5 
MAX_RETRIES = 5

logging.basicConfig(level=logging.INFO)

async def establish_rabbitmq_connection():
    try:
        connection = await aio_pika.connect_robust(
            f"amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}/"
        )
        logging.info("Connected to RabbitMQ")
        return connection
    except Exception as e:
        logging.error(f"Failed to establish RabbitMQ connection: {str(e)}")
        raise

def get_rabbitmq_connection(retries=5, delay=5):
    """Attempts to connect to RabbitMQ with retry logic."""
    for attempt in range(retries):
        try:
            credentials = pika.PlainCredentials(BROKER_USER, BROKER_PASSWORD)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=BROKER_HOST, port=BROKER_PORT, virtual_host=BROKER_VIRTUAL_HOST, credentials=credentials)
            )
            logging.info("Connected to RabbitMQ")
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}. Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
            time.sleep(delay)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
    logging.error("Max retries reached. RabbitMQ connection failed.")
    return None
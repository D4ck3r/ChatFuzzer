import configparser
from aio_pika import connect, IncomingMessage
from aio_pika.exceptions import ProbableAuthenticationError, AMQPConnectionError
import logging  
from utils import utils
import asyncio

class AsyncRabbitMQConsumer:
    def __init__(self):
        self.config = utils.global_config
        self.rabbitmq_url = self.config['RabbitMQ']['url']
        self.queue_name = self.config['RabbitMQ']['queue_name']
        self.connection = None
        self.channel = None

    async def on_message(self, message: IncomingMessage):
        async with message.process():
            await utils.raw_http_queue.put(message.body.decode())
            utils.display.info_vars["Request From Web"] += 1
            # logging.info(f"Received message: {message.body.decode()}")
    async def connect(self):
        while True:
            await asyncio.sleep(1)
            try:
                self.connection = await connect(self.rabbitmq_url)
                self.channel = await self.connection.channel()
                logging.info("Connected to RabbitMQ.")
            except ProbableAuthenticationError:
                logging.error("Failed to authenticate with RabbitMQ.")
            except AMQPConnectionError:
                logging.error("Failed to connect to RabbitMQ.")
            except Exception as e:
                logging.exception(f"An unexpected error occurred: {str(e)}")
            if self.channel:
                break

    async def start_consuming(self):
        if not self.channel:
            await self.connect()
        try:
            queue = await self.channel.declare_queue(self.queue_name, durable=True)
            await queue.consume(self.on_message)
            logging.info(f"Started consuming from '{self.queue_name}' queue.")
        except Exception as e:
            logging.error(f"Failed to start consuming: {str(e)}")

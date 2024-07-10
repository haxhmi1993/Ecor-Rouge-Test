import pika
import time
import os
from utils.logger import logger

class Consumer:
    
    def __init__(self, host="localhost", queue_name="task_queue"):
        """
        Constructor.

        Args:
            host (str): The hostname of the RabbitMQ server.
            queue_name (str): The name of the queue to publish messages to.
        """
        self.host = host
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    def connect(self):
        """
        It establishes connection to RabbitMQ
        """
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        logger.info(" [*] Waiting for messages. To exit press CTRL+C")

    def callback(self, ch, method, properties, body):
        """
        Callback function.

        Args:
            ch (pika.channel.Channel): The channel object.
            method (pika.spec.Basic.Deliver): The basic deliver method.
            properties (pika.spec.BasicProperties): The properties of the message.
            body (bytes): The message body.
        """
        logger.info(f" [x] Received {body.decode()}")
        time.sleep(body.count(b'.'))
        logger.info(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        """
        It consumes messages coming from the Queue
        """
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
        self.channel.start_consuming()

    def close(self):
        """
        It closes connection from RabbitMQ
        """
        self.connection.close()

if __name__ == "__main__":
    rabbitmq_host = os.environ.get("RABBITMQ_HOST", "rabbitmq") or "rabbitmq"
    consumer = Consumer(host=rabbitmq_host)
    consumer.connect()
    try:
        consumer.start_consuming()
    except KeyboardInterrupt:
        logger.info("Interrupted")
    finally:
        consumer.close()
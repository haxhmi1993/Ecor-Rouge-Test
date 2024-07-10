from datetime import datetime
import schedule
import pika
import uuid
import json
import os
from utils.logger import logger

class Producer:
    
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

    def publish_message(self, message):
        """
        It publishes messages to the queue.

        Args:
            message (str): The message to be published.
        """
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        logger.info(f"PRODUCER: [x] Sent '{message}'")

    def close(self):
        """
        It closes connection from RabbitMQ
        """
        self.connection.close()
    
def publisher(producer):
    """
    Publish function for scheduler.

    Args:
        producer (Producer): Producer object.
    """
    message = {"message_id": str(uuid.uuid4()),
               "created_on": str(datetime.now())}
    message = json.dumps(message)
    producer.publish_message(message)
    

if __name__ == "__main__":
    rabbitmq_host = os.environ.get("RABBITMQ_HOST", "rabbitmq") or "rabbitmq"
    poll_interval = os.environ.get("POLL_INTERVAL", 5) or 5
    producer = Producer(host=rabbitmq_host)
    producer.connect()
    (schedule.every(int(poll_interval)).seconds
     .do(publisher,
         producer=producer))
    while True:
        schedule.run_pending()
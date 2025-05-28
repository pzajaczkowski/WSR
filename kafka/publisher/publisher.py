import psutil
import os
from kafka import KafkaProducer
import json
from dotenv import load_dotenv
import logging
import time
import random

load_dotenv()

KAFKA_SERVER = os.getenv("KAFKA_SERVER")
KAFKA_PORT = os.getenv("KAFKA_PORT")
KAFKA_BROKER = f"{KAFKA_SERVER}:{KAFKA_PORT}"
TOPIC = os.getenv("KAFKA_TOPIC_NAME")
PUBLISHER_ID = os.getenv("PUBLISHER_ID")
publisher = f"publisher_{PUBLISHER_ID}"

random.seed(PUBLISHER_ID)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(publisher)
logger.info(f"Connecting to Kafka broker at {KAFKA_BROKER}, topic: {TOPIC}")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    client_id=publisher,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def get_performance_metrics():
    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "publisher": publisher,
    }


def get_fake_performance_metrics():
    return {
        "cpu_percent": random.randint(0, 100),
        "memory_percent": random.randint(0, 100),
        "publisher": publisher,
    }


def send_metrics():
    while True:
        # normally i would use this function but docker containers use
        # host resources and psutil show same metrics for all containers
        # so i just use different seed and take random values as cpu and memory
        # metrics = get_performance_metrics()
        metrics = get_fake_performance_metrics()
        logger.info(f"Sending metrics {metrics}")
        producer.send(TOPIC, metrics)
        time.sleep(3)


if __name__ == "__main__":
    try:
        send_metrics()
    except KeyboardInterrupt:
        logger.info("Stopping publisher.")
    finally:
        producer.close()

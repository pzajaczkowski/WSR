import psutil
import os
from kafka import KafkaProducer
import json
from dotenv import load_dotenv
import logging

load_dotenv()

KAFKA_SERVER = os.getenv("KAFKA_SERVER")
KAFKA_PORT = os.getenv("KAFKA_PORT")
KAFKA_BROKER = f"{KAFKA_SERVER}:{KAFKA_PORT}"
TOPIC = os.getenv("KAFKA_TOPIC_NAME")
PUBLISHER_ID = os.getenv("PUBLISHER_ID")
publisher = f"publisher_{PUBLISHER_ID}"

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
        "cpu_percent": psutil.cpu_percent(interval=3),
        "memory_percent": psutil.virtual_memory().percent,
        "publisher": publisher,
    }


def send_metrics():
    while True:
        metrics = get_performance_metrics()
        logger.info(f"Sending metrics consumer {metrics}")
        producer.send(TOPIC, metrics)


if __name__ == "__main__":
    try:
        send_metrics()
    except KeyboardInterrupt:
        logger.info("Stopping metrics publisher.")
    finally:
        producer.close()

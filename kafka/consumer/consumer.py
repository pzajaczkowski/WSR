from kafka import KafkaConsumer
import json
import logging
import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_SERVER = os.getenv("KAFKA_SERVER")
KAFKA_PORT = os.getenv("KAFKA_PORT")
KAFKA_BROKER = f"{KAFKA_SERVER}:{KAFKA_PORT}"
TOPIC = os.getenv("KAFKA_TOPIC_NAME")
THRESHOLD = 80  # Threshold for high usage in percent

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("Consumer")
logger.info(f"Connecting to Kafka broker at {KAFKA_BROKER}, topic: {TOPIC}")


consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    client_id="Consumer",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)


def calculate_average_usage(metrics_list, metric):
    total_metric = sum(metrics[metric] for metrics in metrics_list)
    total_nodes = len(metrics_list)
    return total_metric / total_nodes if total_nodes > 0 else 0


def process_metrics():
    node_metrics = {}

    for message in consumer:
        metrics = message.value

        node_metrics[metrics["publisher"]] = {
            "cpu_percent": metrics["cpu_percent"],
            "memory_percent": metrics["memory_percent"],
        }

        avg_cpu = calculate_average_usage(node_metrics.values(), "cpu_percent")
        avg_mem = calculate_average_usage(node_metrics.values(), "memory_percent")

        if avg_cpu > THRESHOLD:
            logger.warning(f"Cluster CPU usage is high: {avg_cpu:.2f}%")
        if avg_mem > THRESHOLD:
            logger.warning(f"Cluster Memory usage is high: {avg_mem:.2f}%")

        node_data = node_metrics[metrics["publisher"]]
        logger.info(
            f"Node {metrics['publisher']}: CPU {node_data['cpu_percent']:.2f}%, Memory {node_data['memory_percent']:.2f}%"
        )


if __name__ == "__main__":
    try:
        process_metrics()
    except KeyboardInterrupt:
        logger.info("Stopping metrics consumer.")
    finally:
        consumer.close()

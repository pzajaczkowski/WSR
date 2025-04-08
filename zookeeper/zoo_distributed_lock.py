import time
import random
import logging
import argparse
from kazoo.client import KazooClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DistributedLockDemo:
    def __init__(self, zk_hosts, client_id):
        self.zk = KazooClient(hosts=zk_hosts)
        self.client_id = client_id
        self.zk.start()
        logger.info(f"{client_id}: Connected to Zookeeper")

    def __del__(self):
        self.zk.stop()
        self.zk.close()

    def run(self):
        lock = self.zk.Lock("/locks/demo-lock")

        while True:
            logger.info(f"{self.client_id}: Requesting lock")
            with lock:
                logger.info(f"Client {self.client_id}: Acquired lock")
                time.sleep(random.uniform(4, 8))
                logger.info(f"Client {self.client_id}: Releasing lock")
            time.sleep(random.uniform(2, 4))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--zk-hosts", default="localhost:2181")

    args = parser.parse_args()

    demo = DistributedLockDemo(args.zk_hosts, args.client_id)
    demo.run()


if __name__ == "__main__":
    main()

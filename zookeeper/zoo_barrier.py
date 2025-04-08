import logging
import argparse
from kazoo.client import KazooClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BarrierDemo:
    def __init__(self, zk_hosts, client_id):
        self.zk = KazooClient(hosts=zk_hosts)
        self.client_id = client_id
        self.zk.start()
        logger.info(f"{client_id}: Connected to Zookeeper")

    def __del__(self):
        self.zk.stop()
        self.zk.close()

    def run(self):
        barrier = self.zk.Barrier("/barriers/demo-barrier")

        logger.info(f"{self.client_id}: Waiting at barrier")
        barrier.wait()
        logger.info(f"{self.client_id}: Passed barrier")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--zk-hosts", default="localhost:2181")

    args = parser.parse_args()

    demo = BarrierDemo(args.zk_hosts, args.client_id)
    demo.run()


if __name__ == "__main__":
    main()

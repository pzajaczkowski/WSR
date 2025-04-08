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
        logger.info(f"Client {client_id}: Connected to Zookeeper")
        self.barrier = self.zk.Barrier("/barriers/demo-barrier")

    def __del__(self):
        self.zk.stop()
        self.zk.close()

    def run_create_wait(self):
        logger.info(f"Client {self.client_id}: Creating barrier")
        self.barrier.create()
        logger.info(f"Client {self.client_id}: Barrier created")
        self.run_wait()
        
    def run_wait(self):
        logger.info(f"Client {self.client_id}: Waiting at barrier")
        self.barrier.wait()
        logger.info(f"Client {self.client_id}: Passed barrier")

    def run_delete(self):
        logger.info(f"Client {self.client_id}: Deleting barrier")
        self.barrier.remove()
        logger.info(f"Client {self.client_id}: Barrier deleted")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--mode", choices=["create", "wait", "delete"], default="wait")
    parser.add_argument("--zk-hosts", default="localhost:2181")

    args = parser.parse_args()

    demo = BarrierDemo(args.zk_hosts, args.client_id)

    if args.mode == "create":
        demo.run_create_wait()
    elif args.mode == "wait":
        demo.run_wait()
    elif args.mode == "delete":
        demo.run_delete()
    else:
        logger.error("Invalid mode selected. Use 'wait' or 'delete'.")


if __name__ == "__main__":
    main()

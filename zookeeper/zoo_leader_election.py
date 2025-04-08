import time
import logging
import argparse
from kazoo.client import KazooClient
from kazoo.recipe.election import Election

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LeaderElectionDemo:
    def __init__(self, zk_hosts, client_id):
        self.zk = KazooClient(hosts=zk_hosts)
        self.client_id = client_id
        self.zk.start()
        logger.info(f"{client_id}: Connected to Zookeeper")

    def __del__(self):
        self.zk.stop()
        self.zk.close()

    def run(self):
        election = Election(self.zk, "/elections/demo-election", self.client_id)

        def on_leader():
            logger.info(f"{self.client_id}: I am the leader!")
            time.sleep(5)  # Simulate some work as leader

        election.run(on_leader)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--zk-hosts", default="localhost:2181")

    args = parser.parse_args()

    demo = LeaderElectionDemo(args.zk_hosts, args.client_id)
    demo.run()


if __name__ == "__main__":
    main()

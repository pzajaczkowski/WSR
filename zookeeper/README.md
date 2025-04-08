## Running the Demo

### 1. Distributed Lock Demo

Open multiple terminal windows and run:

```bash
# Terminal 1
python zookeeper_demo.py --mode lock --client-id client1

# Terminal 2
python zookeeper_demo.py --mode lock --client-id client2
```

You should see messages showing when each client requests, acquires, and releases the lock. Only one client can hold the lock at a time.

### 2. Barrier Demo

Open multiple terminal windows and run:

```bash
# Terminal 1
python zookeeper_demo.py --mode barrier --client-id client1

# Terminal 2
python zookeeper_demo.py --mode barrier --client-id client2
```

All clients will wait at the barrier until all participants have arrived, then they'll all proceed together.

### 3. Leader Election Demo

Open multiple terminal windows and run:

```bash
# Terminal 1
python zookeeper_demo.py --mode leader --client-id client1

# Terminal 2
python zookeeper_demo.py --mode leader --client-id client2
```

One client will be elected as the leader. If you stop that client, another will automatically become the leader.

## Simulating Multiple Computers

To simulate multiple computers, you can:

1. Use different machines in your network:
   - Make sure the machines can reach each other
   - Use the IP address of the machine running Zookeeper:
   ```bash
   python zookeeper_demo.py --mode lock --client-id client1 --zk-hosts "zookeeper-ip:2181"
   ```

2. Use Docker containers for clients:
   ```bash
   # Create a Dockerfile for the client
   FROM python:3.9
   WORKDIR /app
   COPY . .
   RUN pip install -r requirements.txt
   CMD ["python", "zookeeper_demo.py", "--mode", "lock", "--client-id", "docker-client"]
   ```

3. Use virtual machines with different IP addresses

## Cleaning Up

To stop and remove the Zookeeper container:
```bash
docker-compose down
```

## Troubleshooting

1. If you can't connect to Zookeeper:
   - Check if the Zookeeper container is running: `docker-compose ps`
   - Verify the port is exposed: `netstat -tulpn | grep 2181`
   - Check Zookeeper logs: `docker-compose logs zookeeper`

2. If you get connection errors:
   - Make sure the Zookeeper host address is correct
   - Check if there are any firewall rules blocking the connection
   - Verify network connectivity between machines

3. If the demo isn't working as expected:
   - Check the Python logs for error messages
   - Verify all clients are using the same Zookeeper path
   - Make sure the Zookeeper container has enough resources allocated 
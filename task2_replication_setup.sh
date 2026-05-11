#!/bin/bash

echo "=== TASK 2: MONGODB REPLICATION SETUP ==="
echo "This script provides instructions on setting up a MongoDB replica set using Docker."
echo "Ensure Docker and Docker Compose are installed on your system."

cat << 'EOF' > docker-compose.yml
version: '3.8'

services:
  mongo1:
    image: mongo:7.0
    container_name: mongo1
    command: ["--replSet", "rs0", "--bind_ip_all", "--port", "27017"]
    ports:
      - "27017:27017"
    volumes:
      - mongo1_data:/data/db

  mongo2:
    image: mongo:7.0
    container_name: mongo2
    command: ["--replSet", "rs0", "--bind_ip_all", "--port", "27018"]
    ports:
      - "27018:27018"
    volumes:
      - mongo2_data:/data/db

  mongo3:
    image: mongo:7.0
    container_name: mongo3
    command: ["--replSet", "rs0", "--bind_ip_all", "--port", "27019"]
    ports:
      - "27019:27019"
    volumes:
      - mongo3_data:/data/db

volumes:
  mongo1_data:
  mongo2_data:
  mongo3_data:
EOF

echo "1. Creating docker-compose.yml for 3 nodes (Primary + 2 Secondaries)."
echo "Run 'docker-compose up -d' to start the containers."
echo ""
echo "2. Initialize the replica set:"
echo "Run this command after containers are up:"
echo "docker exec -it mongo1 mongosh --eval \"rs.initiate({_id: 'rs0', members: [{_id: 0, host: 'mongo1:27017'}, {_id: 1, host: 'mongo2:27018'}, {_id: 2, host: 'mongo3:27019'}]})\""
echo ""
echo "3. Check replication status:"
echo "docker exec -it mongo1 mongosh --eval \"rs.status()\""
echo ""
echo "4. Demonstrate failover:"
echo "docker stop mongo1"
echo "docker exec -it mongo2 mongosh --eval \"rs.status()\""
echo "(Observe that mongo2 or mongo3 becomes the new PRIMARY)"

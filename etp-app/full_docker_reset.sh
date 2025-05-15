#!/bin/bash

echo "🚨 This will delete ALL Docker containers, images, volumes, networks, and builder cache."
read -p "Are you sure? (y/N): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Aborted."
    exit 1
fi

# Stop and remove all containers
docker stop $(docker ps -q) 2>/dev/null
docker rm $(docker ps -aq) 2>/dev/null

# Remove all Docker images
docker image prune -a -f

# Remove all Docker volumes
docker volume prune -f

# Remove all Docker networks
docker network prune -f

# Remove all build cache
docker builder prune -f

# Try docker compose down in case you're in a project folder
docker compose down --volumes --remove-orphans || true

echo "✅ Docker has been reset."

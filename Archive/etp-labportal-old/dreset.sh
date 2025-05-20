#!/bin/bash

# Go to your project directory first
cd /Users/spencer/Projects/etp-app

# Shut down and remove resources from docker-compose
docker compose down --volumes --remove-orphans

# Remove only images built for this project
docker image prune -f

# (Optional) Clear any named volumes you might have
docker volume prune -f

# (Optional) Clear build cache if rebuilds are acting weird
docker builder prune -f


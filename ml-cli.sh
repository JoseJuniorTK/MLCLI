#!/bin/bash

# This script wraps docker compose exec to make CLI usage more intuitive
# Usage: ./ml-cli.sh [command] [args...]

# Check if the container is running
if ! docker ps | grep -q mlcli; then
    echo "Starting mlcli container..."
    docker compose up -d mlcli
fi

# Run the command
docker compose exec mlcli python cli.py "$@" 
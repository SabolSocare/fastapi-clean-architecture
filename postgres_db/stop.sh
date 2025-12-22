#!/bin/bash

# Stop PostgreSQL and pgAdmin containers
# This script stops the Docker containers for the database

echo "🛑 Stopping PostgreSQL Database..."
echo ""

# Change to the script directory
cd "$(dirname "$0")"

# Stop containers
docker-compose down

echo ""
echo "✅ PostgreSQL Database stopped!"
echo ""
echo "💡 To start again: ./start.sh or docker-compose up -d"


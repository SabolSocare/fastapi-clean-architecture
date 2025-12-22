#!/bin/bash

# Check status of PostgreSQL and pgAdmin containers
# This script shows the status of Docker containers

echo "📊 PostgreSQL Database Status"
echo ""

# Change to the script directory
cd "$(dirname "$0")"

# Show container status
docker-compose ps

echo ""
echo "💡 Commands:"
echo "   - Start: ./start.sh"
echo "   - Stop: ./stop.sh"
echo "   - Restart: ./restart.sh"
echo "   - Logs: docker-compose logs -f"


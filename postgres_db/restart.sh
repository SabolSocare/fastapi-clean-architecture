#!/bin/bash

# Restart PostgreSQL and pgAdmin containers
# This script restarts the Docker containers for the database

echo "🔄 Restarting PostgreSQL Database..."
echo ""

# Change to the script directory
cd "$(dirname "$0")"

# Restart containers
docker-compose restart

echo ""
echo "✅ PostgreSQL Database restarted!"
echo ""
echo "📊 Services:"
echo "   - PostgreSQL: localhost:5432"
echo "   - pgAdmin (Web UI): http://localhost:5050"


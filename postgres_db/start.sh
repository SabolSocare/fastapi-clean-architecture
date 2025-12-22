#!/bin/bash

# Start PostgreSQL and pgAdmin containers
# This script starts the Docker containers for the database

echo "🚀 Starting PostgreSQL Database..."
echo ""

# Change to the script directory
cd "$(dirname "$0")"

# Start containers
docker-compose up -d

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Check if containers are running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "✅ PostgreSQL Database is running!"
    echo ""
    echo "📊 Services:"
    echo "   - PostgreSQL: localhost:5432"
    echo "   - pgAdmin (Web UI): http://localhost:5050"
    echo ""
    echo "🔐 pgAdmin Login:"
    echo "   Email: admin@admin.com"
    echo "   Password: admin"
    echo ""
    echo "💡 To view database tables in Chrome:"
    echo "   1. Open http://localhost:5050"
    echo "   2. Login with credentials above"
    echo "   3. Add server: postgres:5432"
    echo "   4. Browse your tables!"
    echo ""
    echo "🛑 To stop: ./stop.sh or docker-compose down"
else
    echo ""
    echo "❌ Failed to start containers"
    echo "Check logs with: docker-compose logs"
    exit 1
fi


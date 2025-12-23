#!/bin/bash
# Database migration script
# Usage: ./migrate.sh [upgrade|downgrade|revision|history]

set -e

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

case "${1:-upgrade}" in
    upgrade)
        echo "Running database migrations..."
        alembic upgrade head
        ;;
    downgrade)
        if [ -z "$2" ]; then
            echo "Usage: ./migrate.sh downgrade [revision]"
            echo "Example: ./migrate.sh downgrade -1  (downgrade one revision)"
            exit 1
        fi
        echo "Downgrading database..."
        alembic downgrade "$2"
        ;;
    revision)
        if [ -z "$2" ]; then
            echo "Usage: ./migrate.sh revision [message]"
            echo "Example: ./migrate.sh revision 'Add phone field to users'"
            exit 1
        fi
        echo "Creating new migration..."
        alembic revision --autogenerate -m "$2"
        ;;
    history)
        echo "Migration history:"
        alembic history
        ;;
    current)
        echo "Current database revision:"
        alembic current
        ;;
    *)
        echo "Usage: ./migrate.sh [upgrade|downgrade|revision|history|current]"
        echo ""
        echo "Commands:"
        echo "  upgrade              - Apply all pending migrations"
        echo "  downgrade [revision] - Downgrade to a specific revision"
        echo "  revision [message]   - Create a new migration"
        echo "  history              - Show migration history"
        echo "  current              - Show current database revision"
        exit 1
        ;;
esac


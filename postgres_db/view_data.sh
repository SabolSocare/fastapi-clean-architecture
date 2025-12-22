#!/bin/bash

# View data in users table
# This script shows all users in the database

echo "📊 Users Table Data"
echo "=================="
echo ""

docker exec fastapi_postgres psql -U postgres -d fastapi_db -c "SELECT id, email, username, is_active, created_at FROM users ORDER BY id;"

echo ""
echo "💡 To view in pgAdmin:"
echo "   1. Open http://localhost:5050"
echo "   2. Connect to 'FastAPI Local DB'"
echo "   3. Navigate: Databases → fastapi_db → Schemas → public → Tables → users"
echo "   4. Right-click 'users' → 'View/Edit Data' → 'All Rows'"
echo ""


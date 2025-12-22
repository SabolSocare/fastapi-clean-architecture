#!/bin/bash

# Add test data to the users table
# This script inserts sample users into the database

echo "📝 Adding test data to users table..."
echo ""

# Insert test users
docker exec fastapi_postgres psql -U postgres -d fastapi_db << EOF
-- Insert test users (if they don't exist)
INSERT INTO users (email, username, hashed_password, is_active) 
VALUES 
    ('john@example.com', 'john_doe', 'hashed_password_123', true),
    ('jane@example.com', 'jane_smith', 'hashed_password_456', true),
    ('admin@example.com', 'admin', 'hashed_password_789', true)
ON CONFLICT (email) DO NOTHING;

-- Show all users
SELECT id, email, username, is_active, created_at FROM users;
EOF

echo ""
echo "✅ Test data added!"
echo ""
echo "💡 View data in pgAdmin:"
echo "   1. Open http://localhost:5050"
echo "   2. Connect to database"
echo "   3. Right-click 'users' table → 'View/Edit Data' → 'All Rows'"
echo ""


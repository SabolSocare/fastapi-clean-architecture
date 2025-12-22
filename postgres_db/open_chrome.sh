#!/bin/bash

# Open pgAdmin in Chrome browser
# This script opens the pgAdmin web interface in Chrome

echo "🌐 Opening pgAdmin in Chrome..."
echo ""

# Wait a moment for pgAdmin to be ready
sleep 2

# Open Chrome with pgAdmin URL
# macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    open -a "Google Chrome" http://localhost:5050
# Linux
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    google-chrome http://localhost:5050 2>/dev/null || chromium-browser http://localhost:5050 2>/dev/null || xdg-open http://localhost:5050
# Windows (Git Bash)
elif [[ "$OSTYPE" == "msys" ]]; then
    start chrome http://localhost:5050
else
    echo "Please open http://localhost:5050 in your browser"
fi

echo ""
echo "✅ pgAdmin should open in Chrome!"
echo ""
echo "🔐 Login Credentials:"
echo "   Email: admin@admin.com"
echo "   Password: admin"
echo ""
echo "📋 To connect to database:"
echo "   1. Right-click 'Servers' → 'Register' → 'Server'"
echo "   2. Name: FastAPI Local DB"
echo "   3. Connection → Host: postgres, Port: 5432"
echo "   4. Database: fastapi_db, User: postgres, Password: postgres123"
echo "   5. Click 'Save'"
echo ""


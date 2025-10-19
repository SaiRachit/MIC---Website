#!/bin/bash

# Railway startup script
echo "🚀 Starting MAHE Innovation Centre Application..."

# Get port from Railway environment variable
PORT=${PORT:-5000}
echo "📍 Using port: $PORT"

# Start the application with gunicorn
echo "🚀 Starting gunicorn server..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 wsgi:app

#!/bin/bash
set -e  # exit on error

echo "🚀 Starting MAHE Innovation Centre Application..."

# Validate PORT
if [ -z "$PORT" ]; then
  echo "⚠️  PORT not set, defaulting to 5000"
  PORT=5000
fi

echo "📍 Using port: $PORT"

# Start Gunicorn server
exec gunicorn --bind 0.0.0.0:${PORT} --workers 4 --timeout 120 wsgi:app

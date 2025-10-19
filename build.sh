#!/usr/bin/env bash
# Build script for Render deployment

echo "Starting build process for MIC Innovation website..."

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Initialize database
echo "Initializing production database..."
python init_production_db.py

echo "Build completed successfully!"

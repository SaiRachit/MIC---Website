#!/usr/bin/env python3
"""
Database setup script for MIC Innovation website
This script helps set up PostgreSQL database and create necessary tables
"""

import os
import sys
import subprocess
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_postgresql_installed():
    """Check if PostgreSQL is installed and running"""
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ PostgreSQL is installed: {result.stdout.strip()}")
            return True
        else:
            print("✗ PostgreSQL is not installed or not in PATH")
            return False
    except FileNotFoundError:
        print("✗ PostgreSQL is not installed or not in PATH")
        return False

def create_database():
    """Create the database if it doesn't exist"""
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("✗ DATABASE_URL not found in environment variables")
        return False
    
    if not db_url.startswith('postgresql://'):
        print("ℹ Using SQLite database (no PostgreSQL setup needed)")
        return True
    
    # Extract database connection details
    # Format: postgresql://username:password@host:port/database
    try:
        # Parse the URL to get connection details
        url_parts = db_url.replace('postgresql://', '').split('@')
        if len(url_parts) != 2:
            print("✗ Invalid DATABASE_URL format")
            return False
        
        user_pass = url_parts[0].split(':')
        if len(user_pass) != 2:
            print("✗ Invalid DATABASE_URL format")
            return False
        
        username, password = user_pass
        host_port_db = url_parts[1].split('/')
        if len(host_port_db) != 2:
            print("✗ Invalid DATABASE_URL format")
            return False
        
        host_port = host_port_db[0].split(':')
        host = host_port[0]
        port = host_port[1] if len(host_port) > 1 else '5432'
        database = host_port_db[1]
        
        print(f"ℹ Attempting to create database: {database}")
        print(f"ℹ Host: {host}, Port: {port}, User: {username}")
        
        # Connect to PostgreSQL server (not specific database)
        server_url = f"postgresql://{username}:{password}@{host}:{port}/postgres"
        
        try:
            engine = create_engine(server_url)
            with engine.connect() as conn:
                # Check if database exists
                result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{database}'"))
                if result.fetchone():
                    print(f"✓ Database '{database}' already exists")
                else:
                    # Create database
                    conn.execute(text(f"CREATE DATABASE {database}"))
                    print(f"✓ Database '{database}' created successfully")
                
                # Commit the transaction
                conn.commit()
                
        except OperationalError as e:
            print(f"✗ Error connecting to PostgreSQL: {e}")
            print("ℹ Make sure PostgreSQL is running and credentials are correct")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Error parsing DATABASE_URL: {e}")
        return False

def test_database_connection():
    """Test the database connection"""
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("✗ DATABASE_URL not found in environment variables")
        return False
    
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✓ Database connection successful")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def create_tables():
    """Create database tables using Flask app context"""
    try:
        from app import app, db
        
        with app.app_context():
            db.create_all()
            print("✓ Database tables created successfully")
            return True
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 MIC Innovation Database Setup")
    print("=" * 40)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("✗ .env file not found. Please create one first.")
        return False
    
    # Check PostgreSQL installation
    if os.environ.get('DATABASE_URL', '').startswith('postgresql://'):
        if not check_postgresql_installed():
            print("\n📋 To install PostgreSQL on Windows:")
            print("1. Download from https://www.postgresql.org/download/windows/")
            print("2. Install with default settings")
            print("3. Remember the password you set for the 'postgres' user")
            print("4. Add PostgreSQL bin directory to your PATH")
            print("5. Update the DATABASE_URL in .env file with your credentials")
            return False
    
    # Create database
    if not create_database():
        return False
    
    # Test connection
    if not test_database_connection():
        return False
    
    # Create tables
    if not create_tables():
        return False
    
    print("\n🎉 Database setup completed successfully!")
    print("You can now run your Flask application.")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

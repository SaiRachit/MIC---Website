#!/usr/bin/env python3
"""
Railway startup script - handles all initialization and error checking
"""

import os
import sys

def check_dependencies():
    """Check if all required packages are available"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask',
        'flask_sqlalchemy', 
        'flask_cors',
        'werkzeug',
        'whitenoise'
    ]
    
    optional_packages = [
        'groq',
        'psycopg2'
    ]
    
    missing_required = []
    missing_optional = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_required.append(package)
            print(f"❌ {package} - REQUIRED")
    
    for package in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_optional.append(package)
            print(f"⚠️ {package} - Optional")
    
    if missing_required:
        print(f"❌ Missing required packages: {missing_required}")
        return False
    
    if missing_optional:
        print(f"⚠️ Missing optional packages: {missing_optional}")
    
    return True

def check_environment():
    """Check environment variables"""
    print("\n🔍 Checking environment variables...")
    
    required_vars = []
    optional_vars = [
        'DATABASE_URL',
        'SECRET_KEY', 
        'GroqAPIKey',
        'RAILWAY_ENVIRONMENT'
    ]
    
    for var in required_vars:
        if not os.environ.get(var):
            print(f"❌ {var} - Required")
            return False
        else:
            print(f"✅ {var}")
    
    for var in optional_vars:
        if os.environ.get(var):
            print(f"✅ {var}")
        else:
            print(f"⚠️ {var} - Not set (optional)")
    
    return True

def test_imports():
    """Test critical imports"""
    print("\n🔍 Testing imports...")
    
    try:
        from app import app
        print("✅ App import successful")
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False
    
    try:
        from models import db
        print("✅ Models import successful")
    except Exception as e:
        print(f"❌ Models import failed: {e}")
        return False
    
    try:
        from routes import main_bp, api_bp, admin_bp
        print("✅ Routes import successful")
    except Exception as e:
        print(f"❌ Routes import failed: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🚀 MAHE Innovation Centre - Railway Startup Check")
    print("=" * 50)
    
    # Run all checks
    if not check_dependencies():
        print("\n❌ Dependency check failed!")
        sys.exit(1)
    
    if not check_environment():
        print("\n❌ Environment check failed!")
        sys.exit(1)
    
    if not test_imports():
        print("\n❌ Import test failed!")
        sys.exit(1)
    
    print("\n✅ All startup checks passed!")
    print("🚀 Application ready to start!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

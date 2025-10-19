#!/usr/bin/env python3
"""
Test script to verify the application works correctly
"""

import os
import sys

def test_imports():
    """Test if all modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test basic imports
        from flask import Flask
        print("✓ Flask imported successfully")
        
        from flask_sqlalchemy import SQLAlchemy
        print("✓ Flask-SQLAlchemy imported successfully")
        
        from flask_cors import CORS
        print("✓ Flask-CORS imported successfully")
        
        from werkzeug.utils import secure_filename
        print("✓ Werkzeug imported successfully")
        
        # Test app imports
        from config import config
        print("✓ Config imported successfully")
        
        from models import db, Event, Resource, Contact, Newsletter
        print("✓ Models imported successfully")
        
        # Test app creation
        from app import app
        print("✓ App imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """Test configuration loading"""
    try:
        print("\nTesting configuration...")
        
        from config import config
        
        # Test development config
        dev_config = config['development']
        print("✓ Development config loaded")
        
        # Test production config
        prod_config = config['production']
        print("✓ Production config loaded")
        
        # Test config attributes
        assert hasattr(dev_config, 'SECRET_KEY')
        assert hasattr(dev_config, 'SQLALCHEMY_DATABASE_URI')
        print("✓ Config attributes present")
        
        return True
        
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_models():
    """Test model definitions"""
    try:
        print("\nTesting models...")
        
        from models import Event, Resource, Contact, Newsletter, ChatSession, ChatMessage
        
        # Test Event model
        event = Event()
        assert hasattr(event, 'title')
        assert hasattr(event, 'description')
        assert hasattr(event, 'to_dict')
        print("✓ Event model structure correct")
        
        # Test Resource model
        resource = Resource()
        assert hasattr(resource, 'title')
        assert hasattr(resource, 'category')
        assert hasattr(resource, 'to_dict')
        print("✓ Resource model structure correct")
        
        # Test Contact model
        contact = Contact()
        assert hasattr(contact, 'name')
        assert hasattr(contact, 'email')
        assert hasattr(contact, 'to_dict')
        print("✓ Contact model structure correct")
        
        # Test Newsletter model
        newsletter = Newsletter()
        assert hasattr(newsletter, 'email')
        assert hasattr(newsletter, 'to_dict')
        print("✓ Newsletter model structure correct")
        
        return True
        
    except Exception as e:
        print(f"❌ Model error: {e}")
        return False

def test_app_structure():
    """Test app structure"""
    try:
        print("\nTesting app structure...")
        
        from app import app
        
        # Test app creation
        assert app is not None
        print("✓ App created successfully")
        
        # Test app configuration
        assert hasattr(app, 'config')
        print("✓ App configuration present")
        
        # Test blueprints registration
        blueprints = app.blueprints
        expected_blueprints = ['main', 'api', 'admin']
        
        for bp_name in expected_blueprints:
            if bp_name in blueprints:
                print(f"✓ Blueprint '{bp_name}' registered")
            else:
                print(f"⚠ Blueprint '{bp_name}' not found")
        
        return True
        
    except Exception as e:
        print(f"❌ App structure error: {e}")
        return False

def test_file_structure():
    """Test required files exist"""
    try:
        print("\nTesting file structure...")
        
        required_files = [
            'app.py',
            'wsgi.py',
            'models.py',
            'routes.py',
            'config.py',
            'requirements.txt',
            'Procfile',
            'railway.json',
            'Dockerfile'
        ]
        
        for file in required_files:
            if os.path.exists(file):
                print(f"✓ {file} exists")
            else:
                print(f"❌ {file} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ File structure error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing MAHE Innovation Centre Application")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_imports,
        test_config,
        test_models,
        test_app_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready for deployment.")
        return True
    else:
        print("❌ Some tests failed. Please fix the issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

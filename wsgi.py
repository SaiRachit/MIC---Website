"""
WSGI entry point for Railway deployment
"""
import os
import sys

try:
    from app import app
    print("✅ Application imported successfully")
except Exception as e:
    print(f"❌ Error importing application: {e}")
    sys.exit(1)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting application on port {port}")
    app.run(host='0.0.0.0', port=port)

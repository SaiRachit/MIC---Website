import os
import sys
from pathlib import Path
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Setup paths
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Initialize Flask app with explicit paths
app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR}/instance/mic_innovation.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Import db from models
from models import db, Event, Resource, Contact, Newsletter, ChatSession, ChatMessage

# Initialize extensions with app
db.init_app(app)
migrate = Migrate(app, db)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Create tables
with app.app_context():
    
    # Create tables if they don't exist
    try:
        db.create_all()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")

# Import and register blueprints
try:
    from backend.routes import main_bp, api_bp, admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    print("Blueprints registered successfully")
except Exception as e:
    print(f"Error registering blueprints: {e}")
    raise

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    try:
        return render_template('404.html'), 404
    except:
        return "404 - Page Not Found", 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    try:
        return render_template('500.html'), 500
    except:
        return "500 - Internal Server Error", 500

# Health check endpoint
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'message': 'Application is running'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

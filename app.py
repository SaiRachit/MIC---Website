from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from config import config
from whitenoise import WhiteNoise

# Initialize Flask app
app = Flask(__name__)

# Load configuration based on environment
# For Railway deployment, detect production environment
if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RENDER') or os.environ.get('FLASK_ENV') == 'production':
    config_name = 'production'
else:
    config_name = os.environ.get('FLASK_ENV', 'development')

app.config.from_object(config[config_name])

# Import models first to get db instance
from models import db, Event, Resource, Contact, Newsletter

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# Import routes
from routes import main_bp, api_bp, admin_bp

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/admin')

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure WhiteNoise for static files in production
if config_name == 'production':
    app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Initialize database on startup
with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

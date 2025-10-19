# Railway Deployment Guide for MAHE Innovation Centre

This guide will help you deploy the MAHE Innovation Centre Flask application to Railway.

## 🚀 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **PostgreSQL Database**: Railway will provide this automatically

## 📋 Deployment Steps

### 1. Connect to Railway

1. Go to [railway.app](https://railway.app) and sign in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will automatically detect the Python application

### 2. Configure Environment Variables

In your Railway project dashboard, go to Variables and add:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database

# Application Configuration
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Admin Configuration
ADMIN_EMAIL=admin@mic.com
ADMIN_PASSWORD=your-admin-password

# Upload Configuration
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

### 3. Database Setup

Railway will automatically:
- Create a PostgreSQL database
- Set the `DATABASE_URL` environment variable
- Run database migrations

### 4. Deploy

1. Railway will automatically build and deploy your application
2. The deployment will use the `Dockerfile` and `railway.json` configuration
3. Your app will be available at the provided Railway URL

## 🔧 Configuration Files

### railway.json
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn wsgi:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Dockerfile
The Dockerfile is configured for:
- Python 3.11
- PostgreSQL client
- Static file serving
- Health checks
- Production optimizations

### Procfile
```
web: gunicorn --bind 0.0.0.0:$PORT wsgi:app
```

## 📁 Project Structure

```
MIC-website/
├── app.py                 # Main Flask application
├── wsgi.py               # WSGI entry point
├── models.py             # Database models
├── routes.py             # All routes and API endpoints
├── config.py             # Configuration classes
├── Chatbot.py            # Chatbot functionality
├── requirements.txt      # Python dependencies
├── runtime.txt           # Python version
├── Procfile              # Railway deployment
├── Dockerfile            # Docker configuration
├── railway.json          # Railway configuration
├── init_production_db.py # Database initialization
├── static/               # Static files
│   ├── js/              # JavaScript files
│   └── uploads/         # File uploads
└── templates/            # HTML templates
```

## 🗄️ Database Models

The application includes the following models:
- **Event**: Innovation events and workshops
- **Resource**: Learning resources and toolkits
- **Contact**: Contact form submissions
- **Newsletter**: Email subscriptions
- **ChatSession**: Chatbot sessions
- **ChatMessage**: Chatbot messages

## 🔍 Features

- ✅ RESTful API endpoints
- ✅ Admin dashboard
- ✅ File upload support
- ✅ Newsletter management
- ✅ Contact form handling
- ✅ Chatbot integration
- ✅ Static file serving
- ✅ Database migrations
- ✅ Production-ready configuration

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all files are in the root directory
2. **Database Connection**: Check `DATABASE_URL` environment variable
3. **Static Files**: Verify WhiteNoise configuration
4. **Port Binding**: Ensure app binds to `0.0.0.0:$PORT`

### Logs

View deployment logs in Railway dashboard:
1. Go to your project
2. Click on the service
3. View logs in the "Deployments" tab

### Database Access

To access your PostgreSQL database:
1. Go to Railway dashboard
2. Click on your database service
3. Use the connection details provided

## 🔄 Updates and Maintenance

### Updating the Application

1. Push changes to your GitHub repository
2. Railway will automatically redeploy
3. Check logs for any deployment issues

### Database Migrations

The application includes database initialization scripts:
- `init_production_db.py`: Creates tables and sample data
- `init_database.py`: Development database setup

### Monitoring

Railway provides:
- Application logs
- Performance metrics
- Database monitoring
- Automatic restarts on failure

## 📞 Support

For Railway-specific issues:
- [Railway Documentation](https://docs.railway.app)
- [Railway Community](https://discord.gg/railway)

For application issues:
- Check the application logs
- Verify environment variables
- Test database connectivity

## 🎉 Success!

Once deployed, your MAHE Innovation Centre application will be available at your Railway URL with:
- Full functionality
- PostgreSQL database
- Static file serving
- Admin dashboard
- API endpoints
- Chatbot integration

The application is now production-ready and optimized for Railway deployment!

# Render Deployment Guide

This guide will help you deploy the MIC Innovation website to Render.

## 🚀 Prerequisites

1. **Render Account**: Sign up at https://render.com
2. **GitHub Repository**: Push your code to GitHub
3. **PostgreSQL Database**: Set up a PostgreSQL database on Render

## 📋 Deployment Steps

### Step 1: Prepare Your Repository

1. **Push to GitHub**: Make sure all your code is pushed to GitHub
2. **Verify Files**: Ensure these files are in your repository root:
   - `Procfile`
   - `requirements.txt`
   - `runtime.txt`
   - `wsgi.py`
   - `build.sh`

### Step 2: Create PostgreSQL Database on Render

1. Go to your Render dashboard
2. Click "New +" → "PostgreSQL"
3. Configure your database:
   - **Name**: `mic-innovation-db`
   - **Database**: `mic_innovation`
   - **User**: `mic_user`
   - **Region**: Choose closest to your users
4. Click "Create Database"
5. **Save the connection details** - you'll need them for environment variables

### Step 3: Deploy Web Service

1. Go to your Render dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:

#### Basic Settings:
- **Name**: `mic-innovation-website`
- **Environment**: `Python 3`
- **Region**: Same as your database
- **Branch**: `main` (or your default branch)

#### Build & Deploy:
- **Build Command**: `pip install -r requirements.txt && python init_production_db.py`
- **Start Command**: `gunicorn wsgi:app`

#### Environment Variables:
Add these environment variables in the Render dashboard:

```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here-change-this
DATABASE_URL=postgresql://mic_user:password@hostname:port/mic_innovation
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
ADMIN_EMAIL=admin@mic.com
ADMIN_PASSWORD=your-secure-admin-password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

**Important**: Replace the DATABASE_URL with your actual PostgreSQL connection string from Step 2.

### Step 4: Configure Custom Domain (Optional)

1. In your web service settings, go to "Custom Domains"
2. Add your domain name
3. Follow Render's instructions to configure DNS

## 🔧 Environment Variables Explained

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `production` |
| `SECRET_KEY` | Flask secret key | `your-secret-key` |
| `DATABASE_URL` | PostgreSQL connection | `postgresql://user:pass@host:port/db` |
| `UPLOAD_FOLDER` | File upload directory | `static/uploads` |
| `ADMIN_EMAIL` | Admin login email | `admin@mic.com` |
| `ADMIN_PASSWORD` | Admin password | `secure-password` |
| `MAIL_*` | Email configuration | For contact forms |

## 📁 File Structure for Render

```
backend/
├── Procfile                 # Web process definition
├── requirements.txt         # Python dependencies
├── runtime.txt             # Python version
├── wsgi.py                 # WSGI entry point
├── build.sh                # Build script
├── app.py                  # Main Flask app
├── config.py               # Configuration
├── models.py               # Database models
├── routes.py               # URL routes
├── init_production_db.py   # Database initialization
├── static/                 # Static files
├── templates/              # HTML templates
└── instance/               # Database files (local only)
```

## 🗄️ Database Configuration

### Local Development:
- Uses SQLite (`instance/mic_innovation.db`)
- No additional setup required

### Production (Render):
- Uses PostgreSQL
- Database URL provided by Render
- Tables created automatically on first deployment

## 🚨 Important Notes

1. **Never commit sensitive data** to your repository
2. **Use environment variables** for all configuration
3. **Test locally** before deploying
4. **Monitor logs** in Render dashboard
5. **Set up backups** for your database

## 🔍 Troubleshooting

### Common Issues:

1. **Build Fails**:
   - Check `requirements.txt` for correct versions
   - Verify Python version in `runtime.txt`

2. **Database Connection Error**:
   - Verify `DATABASE_URL` environment variable
   - Check PostgreSQL service is running

3. **Static Files Not Loading**:
   - Ensure `static/` folder is in repository
   - Check file paths in templates

4. **App Crashes on Startup**:
   - Check logs in Render dashboard
   - Verify all environment variables are set

### Debug Commands:

```bash
# Check logs
render logs --service mic-innovation-website

# Check environment variables
render env --service mic-innovation-website

# Restart service
render restart --service mic-innovation-website
```

## 📊 Monitoring

1. **Health Check**: Your app should respond at `https://your-app.onrender.com`
2. **Database**: Monitor database usage in Render dashboard
3. **Logs**: Check application logs for errors
4. **Performance**: Monitor response times and memory usage

## 🔄 Updates and Maintenance

1. **Code Updates**: Push to GitHub, Render auto-deploys
2. **Database Updates**: Use Flask-Migrate for schema changes
3. **Environment Changes**: Update in Render dashboard
4. **Backups**: Regular database backups recommended

## 🎉 Success!

Once deployed, your MIC Innovation website will be available at:
`https://your-app-name.onrender.com`

**Admin Panel**: `https://your-app-name.onrender.com/admin`
- Email: `admin@mic.com`
- Password: Your configured admin password

## 📞 Support

- **Render Documentation**: https://render.com/docs
- **Flask Documentation**: https://flask.palletsprojects.com/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/

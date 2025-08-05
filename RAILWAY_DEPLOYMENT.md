# Railway + Neon Deployment Guide

## Prerequisites
1. Railway account
2. Neon account (for PostgreSQL database)
3. GitHub repository with your Django app

## Step 1: Set up Neon Database
1. Go to [neon.tech](https://neon.tech) and create an account
2. Create a new project
3. Copy the connection string (it looks like: `postgresql://user:password@host:port/database`)

## Step 2: Deploy to Railway
1. Go to [railway.app](https://railway.app) and create an account
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will automatically detect it's a Python app

## Step 3: Configure Environment Variables
In your Railway project dashboard, go to the "Variables" tab and add:

### Required Variables:
```
DATABASE_URL=your_neon_connection_string
SECRET_KEY=your_django_secret_key
DEBUG=False
ALLOWED_HOSTS=.railway.app,your-custom-domain.com
CSRF_TRUSTED_ORIGINS=https://*.railway.app,https://your-custom-domain.com
SITE_URL=https://your-railway-app-url.railway.app
```

### Optional Variables (for email):
```
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
CLOUDINARY_CLOUD_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_cloudinary_key
CLOUDINARY_API_SECRET=your_cloudinary_secret
```

## Step 4: Generate Secret Key
You can generate a Django secret key using:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 5: Deploy
1. Railway will automatically build and deploy your app
2. Check the deployment logs for any errors
3. Your app will be available at the Railway-provided URL

## Step 6: Custom Domain (Optional)
1. In Railway dashboard, go to "Settings" → "Domains"
2. Add your custom domain
3. Update your DNS settings as instructed

## Troubleshooting
- Check Railway logs for deployment errors
- Ensure all environment variables are set correctly
- Verify Neon database connection string
- Make sure `dj-database-url` is in requirements.txt

## Local Testing
To test with Railway environment locally:
```bash
# Set environment variables
export DATABASE_URL="your_neon_connection_string"
export DEBUG=False
export SECRET_KEY="your_secret_key"

# Run the app
python manage.py runserver
``` 
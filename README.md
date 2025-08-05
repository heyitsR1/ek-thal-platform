# Ek Thaal - Food Donation Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.2.4-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Connecting surplus meals to empty plates across Nepal** 🍽️

Ek Thaal is a community-driven food sharing platform that connects those with surplus food to those who need it. Our mission is simple: reduce food waste and spread kindness, one plate at a time.

## 🌟 Features

### For Food Donors
- **Easy Food Listing**: Post surplus food with details like quantity, preparation time, and location
- **Image Upload**: Add photos of your food items
- **Location Services**: Use GPS coordinates for precise location tracking
- **Recurring Donations**: Set up regular food donations
- **Special Instructions**: Add dietary restrictions or handling notes

### For Food Receivers (Organizations)
- **Browse Available Food**: View all approved food listings in your area
- **Distance Filtering**: Filter food by distance from your location
- **Claim System**: Reserve food items with one click
- **Contact Donors**: Direct communication with food donors
- **Rating System**: Rate your experience with donors

### Admin Features
- **Food Approval System**: Admin review and approval of food listings
- **Email Notifications**: Automated notifications for new listings and claims
- **User Management**: Manage donors and receiver organizations
- **Analytics Dashboard**: Track platform usage and impact

## 🚀 Live Demo

Visit our live application: [Ek Thaal on Render](https://ek-thal.onrender.com)

## 🛠️ Technology Stack

- **Backend**: Django 5.2.4
- **Database**: PostgreSQL (Production), SQLite (Development)
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Render.com
- **Email**: SMTP (Gmail)
- **File Storage**: Cloudinary (Production), Local (Development)
- **Static Files**: WhiteNoise

## 📋 Prerequisites

- Python 3.11+
- pip (Python package installer)
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ek-thal.git
cd ek-thal
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
CLOUDINARY_CLOUD_NAME=your-cloudinary-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the application.

## 🏗️ Project Structure

```
ek-thal/
├── app/                    # Main Django application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── admin.py           # Admin interface
│   └── migrations/        # Database migrations
├── ekthal/                # Django project settings
│   ├── settings.py        # Project settings
│   ├── urls.py           # URL configuration
│   └── wsgi.py           # WSGI configuration
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   └── login.html        # Login page
├── static/               # Static files (CSS, JS, images)
├── media/                # User uploaded files
├── requirements.txt      # Python dependencies
├── render.yaml          # Render deployment config
├── build.sh             # Build script for deployment
├── start.sh             # Start script for deployment
└── README.md            # This file
```

## 🚀 Deployment

### Deploy to Render

1. **Fork/Clone** this repository to your GitHub account
2. **Connect** your GitHub repository to Render
3. **Create a new Web Service** on Render
4. **Configure** the following settings:
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `chmod +x start.sh && ./start.sh`
   - **Environment**: Python 3.11

### Environment Variables for Production

Set these environment variables in your Render dashboard:

```env
PYTHON_VERSION=3.11.0
DEBUG=False
SECRET_KEY=your-generated-secret-key
ALLOWED_HOSTS=.onrender.com
CSRF_TRUSTED_ORIGINS=https://*.onrender.com
RENDER=true
DATABASE_URL=your-postgresql-url
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
CLOUDINARY_CLOUD_NAME=your-cloudinary-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
```

### Deploy to Other Platforms

The application can be deployed to any platform that supports Python/Django:

- **Heroku**: Use `Procfile` and `requirements.txt`
- **Railway**: Direct deployment from GitHub
- **DigitalOcean App Platform**: Container deployment
- **AWS Elastic Beanstalk**: Scalable deployment

## 📧 Email Configuration

The platform uses Gmail SMTP for email notifications. Configure your email settings:

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password
3. Update the email settings in `settings.py`

## 🔧 Configuration

### Database

- **Development**: SQLite (default)
- **Production**: PostgreSQL (recommended)

### Static Files

Static files are served using WhiteNoise in production. For development, Django's built-in server handles static files.

### Media Files

- **Development**: Local file system
- **Production**: Cloudinary (configured in settings)

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Team badUSB** - DAV Codefest 2025
- **Django Community** - For the amazing framework
- **Render** - For hosting and deployment
- **Cloudinary** - For media file management

## 📞 Contact

- **Project Link**: [https://github.com/heyitsR1/ek-thal-platform](https://github.com/heyitsR1/ek-thal-platform)
- **Live Demo**: [https://ek-thal.onrender.com](https://ek-thal.onrender.com)

## 🐛 Known Issues

- Email notifications may be delayed in production
- Image upload requires proper Cloudinary configuration
- GPS coordinates require HTTPS in production

## 🔮 Future Enhancements

- [ ] Mobile app development
- [ ] Real-time notifications
- [ ] Advanced search and filtering
- [ ] Food safety guidelines integration
- [ ] Community features and forums
- [ ] Analytics and reporting dashboard

---

**Made with ❤️ for Nepal** 🇳🇵

*One Plate, Many Smiles* 🍽️✨ 
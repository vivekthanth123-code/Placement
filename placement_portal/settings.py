"""
Django settings for placement_portal project.
Upgraded configuration (Dev + Ready for Production tweaks)
"""

from pathlib import Path
import os

# ======================================================
# 📁 BASE DIRECTORY
# ======================================================
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


# ======================================================
# 🔐 SECURITY
# ======================================================
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-change-this-in-production"
)

DEBUG = True  # ⚠️ Set False in production

ALLOWED_HOSTS = ['*']  # Add domain/IP in production


# ======================================================
# 📦 INSTALLED APPS
# ======================================================
INSTALLED_APPS = [
    'portal',

    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


# ======================================================
# 🧠 MIDDLEWARE
# ======================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # ✅ Helps with static files in production (optional but good)
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    # ✅ REQUIRED for login state
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ======================================================
# 🔗 URL CONFIG
# ======================================================
ROOT_URLCONF = 'placement_portal.urls'


# ======================================================
# 🎨 TEMPLATES
# ======================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # ✅ Global templates folder
        'DIRS': [BASE_DIR / "templates"],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',

                # ✅ IMPORTANT for navbar auth check
                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

                'portal.context_processors.user_profile',
            ],
        },
    },
]


# ======================================================
# 🚀 WSGI
# ======================================================
WSGI_APPLICATION = 'placement_portal.wsgi.application'


# ======================================================
# 🗄️ DATABASE
# ======================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}


# ======================================================
# 🔑 PASSWORD VALIDATION
# ======================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ======================================================
# 🌍 INTERNATIONALIZATION
# ======================================================
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'  # ✅ Better for India

USE_I18N = True
USE_TZ = True


# ======================================================
# 📁 STATIC FILES
# ======================================================
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # your project static folder
]

# ======================================================
# 📁 MEDIA FILES (Uploads)
# ======================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ======================================================
# 🔐 AUTH REDIRECTS (VERY IMPORTANT)
# ======================================================
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'student_dashboard'
LOGOUT_REDIRECT_URL = 'login'


# ======================================================
# 🧪 DEFAULT PRIMARY KEY
# ======================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ======================================================
# 📧 EMAIL CONFIGURATION
# ======================================================
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development - prints to console
# For production, use SMTP:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password'

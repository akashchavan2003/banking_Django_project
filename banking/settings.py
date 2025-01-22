import os
from pathlib import Path
from django.urls import reverse_lazy

# Define the base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = 'django-insecure-+#856dxwy%-wd-q5-@xl2)alxs3^vkw(hsje9*1)wp15n%#e=l'
DEBUG = True
ALLOWED_HOSTS = ['banking-django-project.onrender.com', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',  # Add 'allauth' and its dependencies
    'allauth.account',
    'allauth.socialaccount',
    'system.apps.SystemConfig',  # Use only this for your 'system' app
    'debug_toolbar',  # Debug toolbar
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Middleware for allauth
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'banking.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'system.context_processors.custom_context',  # Custom context processor
            ],
        },
    },
]

WSGI_APPLICATION = 'banking.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'other_database': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'bank_manage.db'),
    },
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Media and static files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Authentication settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'system.backend.CustomAuthenticationBackend',  # Custom backend
]

SITE_ID = 1

# URL redirection settings
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT = '/'

# Allauth email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Internal IPs for the debug toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

# Session and security settings
LOGIN_URL = reverse_lazy('login')
SESSION_COOKIE_NAME = 'mybankapp_session'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
DATABASE_ROUTERS = ['system.routers.OtherDatabaseRouter']
CSRF_COOKIE_SECURE = True

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://banking-django-project.onrender.com',
    # Add other trusted origins as needed
]

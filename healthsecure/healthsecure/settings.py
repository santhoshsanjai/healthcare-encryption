import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-$t08wp7#hzauah$lyk=m((_*_2)p_yvt(utlpf2-uzq87r79uh'

DEBUG = True
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'healthapp',      # Your custom app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Required for login/auth
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_SECURE = False  # True only if using HTTPS
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_DOMAIN = None  # Only set if using subdomains
ROOT_URLCONF = 'healthsecure.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',        # Required
                'django.contrib.messages.context_processors.messages',# Required
            ],
        },
    },
]

WSGI_APPLICATION = 'healthsecure.wsgi.application'

# ✅ Database (SQLite for development)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation (optional: for production)
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
USE_TZ = True

# Static files (CSS, JS, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]  # Make sure the folder exists

# Login / Logout URLs
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

LOGIN_URL = '/'

# AUTH_USER_MODEL = 'healthapp.CustomUser'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

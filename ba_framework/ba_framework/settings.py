"""
Django settings for ba_framework project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY is retrieved from environment variables for security
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG mode is controlled via environment variable, defaulting to False in production
if os.environ.get('DJANGO_DEBUG') == "true":
    DEBUG = True
else:
    DEBUG = False

# Allowed hosts for the Django app
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Secure the app behind a proxy with SSL
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Maximum number of fields to accept in a form submission
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000


# Application definition
# Installed apps in the Django project
INSTALLED_APPS = [
    'django.contrib.admin',  # Django admin interface
    'django.contrib.auth',  # Authentication framework
    'django.contrib.contenttypes',  # Content types framework
    'django.contrib.sessions',  # Session framework
    'django.contrib.messages',  # Messaging framework
    'django.contrib.staticfiles',  # Static files handling
    'channels',  # Channels for WebSocket support
    'rest_framework',  # Django REST framework
    'rest_framework.authtoken',  # Token authentication for REST framework
    'logger',  # Custom app named 'logger'
    'agents',  # Custom app named 'agents'
    'rest_api',  # Custom app named 'rest_api'
    'import_export',  # Django Import Export app
    'django_extensions',  # Additional Django extensions
    'django_celery_beat',  # Celery Beat Scheduler
    'django_celery_results'  # Celery Results Backend
]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Security middleware
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session middleware
    'django.middleware.common.CommonMiddleware',  # Common middleware
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection middleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentication middleware
    'django.contrib.messages.middleware.MessageMiddleware',  # Messaging middleware
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection middleware
]

# Root URL configuration
ROOT_URLCONF = 'ba_framework.urls'


# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Template backend
        'DIRS': [],  # Directories to search for templates
        'APP_DIRS': True,  # Search templates in app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Debug context processor
                'django.template.context_processors.request',  # Request context processor
                'django.contrib.auth.context_processors.auth',  # Auth context processor
                'django.contrib.messages.context_processors.messages',  # Messages context processor
            ],
        },
    },
]

# WSGI application
# This setting specifies the full Python path to the WSGI application callable that Django uses to serve your project.
# WSGI (Web Server Gateway Interface) is a specification that allows web servers to communicate with web applications.
# It is the standard for serving Python web applications, ensuring compatibility and easy deployment across different web servers.
# The value 'ba_framework.wsgi.application' points to the 'application' callable in the 'wsgi.py' module of your project.
# This callable is used by WSGI servers (like Gunicorn or uWSGI) to forward requests to your Django application.
WSGI_APPLICATION = 'ba_framework.wsgi.application'

# ASGI application for handling WebSockets
# This setting specifies the full Python path to the ASGI application callable that Django uses to handle asynchronous features like WebSockets.
# ASGI (Asynchronous Server Gateway Interface) is a specification designed to handle asynchronous web protocols.
# It supports handling WebSockets, HTTP/2, and other asynchronous features, making it suitable for modern web applications that require real-time communication.
# The value 'ba_framework.routing.application' points to the 'application' callable in the 'routing.py' module of your project.
# This callable is used by ASGI servers (like Daphne or Uvicorn) to manage asynchronous communication, such as WebSocket connections.
ASGI_APPLICATION = 'ba_framework.routing.application'


# Channel layers configuration
# Channel layers allow for handling real-time events and are used by Django Channels.
# They provide a way to group channels and send messages between them, supporting real-time features like WebSockets.
CHANNEL_LAYERS = {
    'default': {
        # Use Redis as the backend for channel layers.
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            # List of Redis servers to connect to. Here, we use a single Redis server running on the host 'redis' and port 6379.
            "hosts": [('redis', 6379)],
            # Capacity defines the maximum number of messages that can be in a channel at once. If this is exceeded, new messages are discarded.
            "capacity": 1500,
            # Expiry time in seconds for messages in the channel. Messages that are older than this are discarded.
            "expiry": 10,
        },
    },
}

# Cache configuration
# Caching improves the performance of the application by storing frequently accessed data in a faster storage medium.
# Here, we configure Django to use the database as the cache backend.
CACHES = {
    'default': {
        # Use the database for caching.
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        # Name of the database table where the cache will be stored.
        'LOCATION': 'my_cache_table',
    }
}

# Celery result backend configuration
# This specifies where Celery should store the results of tasks. Here, Redis is used as the result backend.
result_backend = 'redis://redis:6379/0'

# Django REST framework settings
# These settings configure the authentication and permission classes for the Django REST framework.
REST_FRAMEWORK = {
    # List of authentication classes used by the REST framework.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # Basic authentication uses HTTP Basic Auth to authenticate users.
        'rest_framework.authentication.BasicAuthentication',
        # Session authentication uses Django's session framework for authentication.
        'rest_framework.authentication.SessionAuthentication',
    ],
    # List of permission classes used by the REST framework.
    'DEFAULT_PERMISSION_CLASSES': [
        # Require all users to be authenticated to access the API.
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'timescale.db.backends.postgresql',
        'NAME': os.environ.get('Postgres_DATABASE'),
        'USER': os.environ.get('Postgres_USER'),
        'PASSWORD': os.environ.get('Postgres_PASSWORD'),
        'HOST': os.environ.get('Postgres_HOST'),
        'PORT': os.environ.get('Postgres_PORT')
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ADMINS setting
# This setting is a list of people who get code error notifications when DEBUG=False.
# When the server encounters an error, an email will be sent to each person listed here.
# Each entry is a tuple containing the name and email address of an admin.
# For more information: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ('Payam Fatehi', 'payam.fatehi@eonerc.rwth-aachen.de')
]

# MANAGERS setting
# This setting is similar to ADMINS but is intended to specify who gets broken link notifications.
# By default, it is set to the same value as ADMINS.
# For more information: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS



# Celery configuration for the timezone in which Celery will operate.
# This should match the timezone used by your Django application to ensure consistency.
CELERY_TIMEZONE = 'Europe/Berlin'

# Enable tracking of the start of tasks.
# This setting helps to monitor when a task starts executing.
CELERY_TASK_TRACK_STARTED = True

# Set a time limit for how long a task can run.
# The value is in seconds, so here it's set to 30 minutes.
CELERY_TASK_TIME_LIMIT = 30 * 60

# Cache backend for Celery.
# Specifies the cache backend to use for storing task results.
CELERY_CACHE_BACKEND = 'default'

# Scheduler for periodic tasks.
# Use the Django database scheduler to store the schedule in the database.
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

# Broker URL for Celery.
# This is the URL of the message broker that Celery will use to send and receive messages.
# Here, Redis is used as the message broker, running on host 'redis' and port 6379.
CELERY_BROKER_URL = 'redis://redis:6379/0'

# Backend for storing task results.
# Specifies where Celery will store the results of tasks.
# Here, task results are stored in the Django database.
CELERY_RESULT_BACKEND = 'django-db'

# Enable extended task result storage.
# This setting allows storing additional metadata about task results.
CELERY_RESULT_EXTENDED = True

# Expiry time for task results.
# Set to None to keep results indefinitely.
# For more information: https://docs.celeryq.dev/en/latest/userguide/configuration.html#result-expires
CELERY_RESULT_EXPIRES = None

# List of content types that Celery will accept.
# Specifies the serialization formats that tasks and results can use.
CELERY_ACCEPT_CONTENT = ['application/json']

# Serializer for task results.
# Specifies how task results should be serialized. Here, JSON is used.
CELERY_RESULT_SERIALIZER = 'json'

# Serializer for task data.
# Specifies how task data should be serialized. Here, JSON is used.
CELERY_TASK_SERIALIZER = 'json'


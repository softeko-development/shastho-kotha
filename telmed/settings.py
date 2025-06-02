# settings.py

import os

from pathlib import Path
from datetime import timedelta
import firebase_admin
from firebase_admin import credentials

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-%pvqo9+w+20lro@baqm$i(4_r9(wy*ot&jzi(s(wiaiwj9m2sv'

DEBUG = True
# ALLOWED_HOSTS = ['shastokotha.com', 'www.shastokotha.com']
ALLOWED_HOSTS = ['*']

# CSRF_TRUSTED_ORIGINS = ['https://shastokotha.com', 'https://www.shastokotha.com']


# Application definition

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,  # Keeps the default configuration of Django's loggers

#     'formatters': {  # Define the format of the logs
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
    
#     'handlers': {  # Define how to handle the logs
#         'file': {
#             'level': 'DEBUG',  # Minimum level of logging handled by this handler
#             'class': 'logging.FileHandler',  # Send logs to a file
#             'filename': os.path.join(BASE_DIR, 'debug.log'),  # Log file location
#             'formatter': 'verbose',  # Use the 'verbose' format
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',  # Print logs to the console
#             'formatter': 'simple',  # Use the 'simple' format
#         },
#     },
    
#     'loggers': {  # Configure loggers for different parts of your application
#         'django': {
#             'handlers': ['file', 'console'],
#             'level': 'DEBUG',  # Minimum level of logging for this logger
#             'propagate': True,  # Propagate logs to parent loggers
#         },
#         'telmed': {  # Replace 'myapp' with your app name
#             'handlers': ['file', 'console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }

FIREBASE_CREDENTIALS_FILE = BASE_DIR / 'firebase_credentials.json'
# FIREBASE_CREDENTIALS_FILE = r'C:\Users\mahta\OneDrive\Desktop\D\telemed\firebase_credentials.json'

if not firebase_admin._apps:  # Check if Firebase Admin SDK is already initialized
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_FILE)
    firebase_admin.initialize_app(cred)

PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_SERVICE_ACCOUNT_PATH": FIREBASE_CREDENTIALS_FILE,
    "UPDATE_ON_DUPLICATE_REG_ID": True,
}

INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_celery_results',
    'corsheaders',
    'import_export',
    'widget_tweaks',
    'channels',
    'push_notifications',
    'user',
    'prescription',
    'conference',
]

ASGI_APPLICATION = 'telmed.asgi.application'

# Channels settings
CHANNEL_LAYERS = {
    'default': {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),  # 30 days
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365*10),  # 10 years
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}


ROOT_URLCONF = 'telmed.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'user.context_processors.doctor_profile_processor',
            ],
            'libraries': {
                'custom_tags': 'user.templatetags.template_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'telmed.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = False


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR/'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'user.CustomUser'

AGORA_APP_ID = 'ae8218aff801440ba01d25cd22820230'
AGORA_APP_CERTIFICATE = 'a21d90e9de9b45a9a6a25007fb9045ac'

# CELERY_BROKER_URL= "redis://127.0.0.1:6379/0"
CELERY_BROKER_URL = "redis://default:jvSHaGqDa6kAKXggd93x3NNV8GD7jV2c@redis-17713.c301.ap-south-1-1.ec2.redns.redis-cloud.com:17713/0"
CELERY_RESULT_BACKEND = "django_celery_results.backends.database:DatabaseBackend"

CELERY_TIMEZONE = "Asia/Dhaka"
CELERY_RESULT_EXTENDED = True
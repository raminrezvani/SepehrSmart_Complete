import os
import environ
from datetime import timedelta
from pathlib import Path
from  hotel_providers_api.admin_setting import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u-i%rgl^l27uw+tg$vm3v8q1haozo*m@&64rgr&)d@ts4_mrpa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', 'tour-collector-api.sepehrsmart.ir', "94.74.182.183"]

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# reading .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env.production'))

# define all environment variables
FRONT_END_URL = env('FRONT_END_URL')
POSTGRESQL_DB_NAME = env('POSTGRESQL_DB_NAME')
POSTGRESQL_USER = env('POSTGRESQL_USER')
POSTGRESQL_PASSWORD = env('POSTGRESQL_PASSWORD')
POSTGRESQL_HOST = env('POSTGRESQL_HOST')
POSTGRESQL_PORT = env('POSTGRESQL_PORT')
REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')
REDIS_PASSWORD = env('REDIS_PASSWORD')
IS_RUNNING_IN_DOCKER = env('IS_RUNNING_IN_DOCKER')
BUILD_TOUR_TIMEOUT = env('BUILD_TOUR_TIMEOUT')
BUILD_TOUR_REFRESH_TIMEOUT = env('BUILD_TOUR_REFRESH_TIMEOUT')

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ---
    'rosetta',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'after_response',
    # ---
    'app_utils',
    'app_crawl',
    'app_api',
    'app_user',
    'app_report',
    'app_company',
    'app_admin',
    "app_hotel"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hotel_providers_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hotel_providers_api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.getenv('DATABASE_PATH', BASE_DIR / 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRESQL_DB_NAME,
        'USER': POSTGRESQL_USER,
        'PASSWORD': POSTGRESQL_PASSWORD,
        'HOST': POSTGRESQL_HOST,
        'PORT': POSTGRESQL_PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = "app_user.User"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static', 'assets')
]

STATIC_ROOT = BASE_DIR / "static" / "Static_Root"

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / "static" / "Static_Media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = [
    "https://tour-collector.sepehrsmart.ir",
    "http://tour-collector.sepehrsmart.ir",
    "https://tour-cookie.sepehrsmart.ir",
    "http://tour-cookie.sepehrsmart.ir",
    'https://tour-collector-api.sepehrsmart.ir',
    'http://tour-collector-api.sepehrsmart.ir',
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # "http://94.74.182.183:8000",
    "http://185.252.31.31:8000",
    "http://185.252.31.31",
    FRONT_END_URL,
    # "http://94.74.182.183"
]


CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS.copy()

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Authorization'


]
CORS_ALLOW_CREDENTIALS = True  # Allow cookies/credentials if your frontend sends them
CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins (for development only)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'hotel_tasks.log',  # Log file path
            'formatter': 'detailed',
        },
    },
    'formatters': {
        'detailed': {
            'format': ' %(message)s',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,

    "ALGORITHM": "HS512",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("JWT",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(days=2),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=3),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

# Provider Service URLs
PROVIDER_SERVICES = {
    'BOOKING': {
        'BASE_URL': 'http://185.252.30.120:3040/',
        'ENDPOINTS': {
            'HOTELS': 'booking_hotels'
        }
    },
    'BOOKING_READYTOUR': {
        'PRIMARY_SERVER': 'http://185.252.30.120:5001/booking_tours',
        'SECONDARY_SERVER': 'http://185.252.30.120:5001/booking_tours',
        'THRESHOLD': 200
    },
    'ALAEDIN': {
        'BASE_URL': 'http://185.252.30.120:5003/',
        'ENDPOINTS': {
            'ROOMS': 'Alaedin_rooms'
        }
    },
    'SNAPP': {
        'BASE_URL': 'http://185.252.30.120:5004/',
        'ENDPOINTS': {
            'HOTELS': 'SnappTrip_Hotelrooms'
        }
    },
    'EGHAMAT24': {
        'BASE_URL': 'http://185.252.30.120:8022/',
        'ENDPOINTS': {
            'HOTELS': 'fetch_hotels'
        }
    },
    'JIMBO': {
        'BASE_URL': 'http://185.252.30.120:3030/',
        'ENDPOINTS': {
            'HOTELS': 'Jimbo_hotels'
        }
    },
    'JIMBO_READYTOUR': {
        'PRIMARY_SERVER': 'http://185.252.30.120:5021/jimbo_tours',
        'SECONDARY_SERVER': 'http://185.252.30.120:5021/jimbo_tours',
        'THRESHOLD': 200
    },
    'SEPEHR': {
        'BASE_URL': 'http://185.252.30.120:5000',
        'ENDPOINTS': {
            'HOTEL_SEARCH': '/api/hotel/search'
        }
    },
    'DELTABAN': {
        'BASE_URL': 'http://185.252.30.120:5002',
        'ENDPOINTS': {
            'HOTEL_SEARCH': '/api/hotel/deltaban/search'
        }
    },
    'ALWIN': {
        'BASE_URL': 'http://185.252.30.120:5055',
        'ENDPOINTS': {
            'HOTELS': 'alwin_hotels'
        }
    }
}

# Redis Configuration
# REDIS_CONFIG = {
#     'HOST': 'localhost',
#     'PORT': 6379,
#     'DB': 0,
#     'DECODE_RESPONSES': True
# }

import psutil
import json
from django.http import JsonResponse

def list_process_threads():
    process = psutil.Process()  # Current process
    threads = process.threads()
    print("process ID:", process.pid)
    print("number of threads:", len(threads))
    thread_info = [{'id': thread.id, 'user_time': thread.user_time, 'system_time': thread.system_time}  for thread in threads]
    # return JsonResponse(thread_info, safe=False)

    # Print thread_info in JSON format with indent=4
    # print(json.dumps(thread_info, indent=4))

    # return thread_info
    return
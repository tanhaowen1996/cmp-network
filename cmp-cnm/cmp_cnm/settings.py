"""
Django settings for cmp_cnm project.

Generated by 'django-admin startproject' using Django 3.2.9.

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
SECRET_KEY = 'django-insecure-pg-2*hls3&x0oz@6tgg-t&2_d5*7+u4mj3ky)fhst)254g_^x('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv('DEBUG', 0)))

ALLOWED_HOSTS = ['*']
APPEND_SLASH = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'cmp_cnm',
    'nssrc',
    'lb',
    'lb.citrixapi',
    'lb.radwareapi',
    'rest_framework',
    'django_apscheduler',
    'route',
    'firewall',
]

REST_FRAMEWORK = {
    'DATE_FORMAT': '%Y-%m-%d',
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DEFAULT_PAGINATION_CLASS': 'cmp_cnm.pagination.PageNumberPagination',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'NON_FIELD_ERRORS_KEY': 'all',
}

MIDDLEWARE = [
    'cmp_cnm.soloveCrossDomain.SoloveCrossDomainMiddleware',
    'cmp_cnm.middleware.HealthCheckMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cmp_cnm.urls'
HEALTH_CHECK_PATH = os.getenv('HEALTH_CHECK_PATH', '/health')

URL = os.getenv("URL", "127.0.0.1:8080")
WEB_PORT = os.getenv("WEB_PORT", 8080)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cmp_cnm.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'cmp_cnm'),
        'USER': os.getenv('DB_USER', 'cmp_cnm'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'cmp_cnm'),
        'HOST': os.getenv('DB_HOST', '10.208.224.79'),
        'PORT': int(os.getenv('DB_PORT', 5432)),
        'CONN_MAX_AGE': 3
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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATETIME_FORMAT = 'Y-m-d H:i:s'

DATE_FORMAT = 'Y-m-d'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

OS_PROJECT_DOMAIN_NAME = os.getenv('OS_PROJECT_DOMAIN_NAME', 'Default')
OS_USER_DOMAIN_NAME = os.getenv('OS_USER_DOMAIN_NAME', 'Default')
OS_PROJECT_NAME = os.getenv('OS_PROJECT_NAME', 'admin')
OS_TENANT_NAME = os.getenv('OS_TENANT_NAME', 'admin')
OS_USERNAME = os.getenv('OS_USERNAME', 'admin')
OS_PASSWORD = os.getenv('OS_PASSWORD', 'NY4E6Tz6SfuKBztPppBik1GXTqY7m3M3FDpsL2nK')
OS_AUTH_URL = os.getenv('OS_AUTH_URL', 'http://10.209.0.10:35357/v3')
OS_INTERFACE = os.getenv('OS_INTERFACE', 'internal')
OS_ENDPOINT_TYPE = os.getenv('OS_ENDPOINT_TYPE', 'internalURL')
OS_IDENTITY_API_VERSION = int(os.getenv('OS_IDENTITY_API_VERSION', '3'))
OS_REGION_NAME = os.getenv('OS_REGION_NAME', 'test')
OS_AUTH_PLUGIN = os.getenv('OS_AUTH_PLUGIN', 'password')
OS_REGION_MAWEI = os.getenv('OS_REGION_MAWEI', 'test')

OS_TOKEN_KEY = os.getenv('OPENSTACK_TOKEN_KEY', 'x-auth-token')

NS_HOST = os.getenv('NS_HOST', '10.209.0.65')
NS_PROTOCOL = os.getenv('NS_PROTOCOL', 'http')
NS_USER = os.getenv('NS_USER', 'nsroot')
NS_PASSWD = os.getenv('NS_PASSWD', 'r00tme')
NS_TIME = os.getenv('NS_TIME', 3600)
HTTP_FILE = os.getenv('HTTP_FILE', '10.208.0.49:8080')
RW_URL = os.getenv('RW_URL', 'https://10.209.0.61')
RW_USER = os.getenv('RW_USER', 'admin')
RW_PASSWD = os.getenv('RW_PASSWD', 'radware')

WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=84889afd-ea6a-49fb-b922-72cc10e99629')

H3C_HOST = os.getenv('H3C_HOST', '10.209.255.2')
H3C_PORT = os.getenv('H3C_PORT', 830)
H3C_USER = os.getenv('H3C_USER', 'fzyh_mawei')
H3C_PASSWORD = os.getenv('H3C_PASSWORD', 'fzyh_mawei_yh601933')

SWAGGER = bool(int(os.getenv('SWAGGER', 0)))

if SWAGGER:
    SWAGGER_SETTINGS = {
        'LOGOUT_URL': '/admin/logout/',
        'SECURITY_DEFINITIONS': {
            OS_TOKEN_KEY: {
                'type': 'apiKey',
                'name': OS_TOKEN_KEY.lower(),
                'in': 'header'
            }
        },
    }

from logs.log_path import LOG_DIR

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'standard': {
            'format': '[%(asctime)s] [%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': open(os.path.join(LOG_DIR, 'cmp-cnm-api.log'), 'a'),
            'formatter': 'standard'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'cmp-cnm.log'),
            'formatter': 'standard'
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'all.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request ': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'cmp_cnm': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


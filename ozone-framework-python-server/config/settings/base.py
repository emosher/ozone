# settings/base.py

"""
Django settings for owf_framework project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import ast

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6_0yi$sofm8lt(oc4l=%1nyxgog#ek0_+eyki_0a3)2_tej3fd'

# SECURITY WARNING: don't run with debug turned on in production!
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

    # 3rd party apps
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'django_filters',
    'method_override',

    # owf apps
    'domain_mappings.apps.DomainMappingsConfig',
    'intents.apps.IntentsConfig',
    'owf_groups.apps.OWFGroupsConfig',
    'people.apps.PeopleConfig',
    'roles.apps.RolesConfig',
    'stacks.apps.StacksConfig',
    'widgets.apps.WidgetsConfig',
    'dashboards.apps.DashboardsConfig',
    'preferences.apps.PreferencesConfig',
    'appconf.apps.AppconfConfig',
    'metrics.apps.MetricsConfig',

]

AUTH_USER_MODEL = 'people.Person'


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'method_override.middleware.MethodOverrideMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'config.owf_utils.log_middleware.LogMiddleware',
    'config.owf_utils.transformer.django.middleware.OwfCaseTransformerMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv('OWF_DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('OWF_DB_NAME', 'postgres'),
        'USER': os.getenv('OWF_DB_USER', 'postgres'),
        'PASSWORD': os.getenv('OWF_DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('OWF_DB_HOST', 'localhost'),
        'PORT': os.getenv('OWF_DB_PORT', '5432'),
        # Wraps each web request in a transaction. So if anything fails, it will rollback automatically.
        'ATOMIC_REQUESTS': True,
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

HELP_FILES = os.path.join(BASE_DIR, 'help_files')
HELP_FILES_URL = '/help_files/'

SYSTEM_VERSION = '2'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100000,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}
# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'config.owf_utils.authentication.DjangoAuthenticateByUsername',
]

LOGIN_REDIRECT_URL = '/api/v2/me/'  # Other option is INFO

#  LOG
if not os.path.exists('./logs'):
    os.mkdir('./logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'ignore_markdown_logs': {
            '()': 'config.owf_utils.owf_logging_backends.MarkDownFilter',
        },
        'ignore_reload_logs': {
            '()': 'config.owf_utils.owf_logging_backends.ReloadFilter',
        },
        'ignore_favicon_logs': {
            '()': 'config.owf_utils.owf_logging_backends.FaviconFilter',
        },
    },
    'formatters': {
        'console': {
            'format': '%(levelname)-8s SHOST: [%(hostname)s] TIME [ %(asctime)s ] %(name)-12s %(message)s ',
            'class': 'config.owf_utils.owf_logging_backends.HostnameAddingFormatter',
        },
        'cef-format': {
            'format': '%(asctime)s CEF shost=%(hostname)s %(message)s ',
            'datefmt': "%d/%b/%Y %H:%M:%S",
            'class': 'config.owf_utils.owf_logging_backends.HostnameAddingFormatter',
        },
        'event-format': {
            'format': '%(levelname)-8s SHOST: [%(hostname)s] TIME [ %(asctime)s ] %(name)-12s %(message)s ',
            'datefmt': "%d/%b/%Y %H:%M:%S",
            'class': 'config.owf_utils.owf_logging_backends.HostnameAddingFormatter',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['ignore_markdown_logs', 'ignore_reload_logs', 'ignore_favicon_logs'],
            'formatter': 'console'
        },
        'cef-file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filters': ['ignore_markdown_logs', 'ignore_reload_logs', 'ignore_favicon_logs'],
            'formatter': 'cef-format',
            'filename': os.getenv('CEF_LOCATION', 'logs') + '/owf-cef.log',
            'maxBytes': 50000,
            'backupCount': 2,
        },
        'event-file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filters': ['ignore_markdown_logs', 'ignore_reload_logs', 'ignore_favicon_logs'],
            'formatter': 'event-format',
            'filename': os.getenv('CEF_LOCATION', 'logs') + '/owf-events.log',
            'maxBytes': 50000,
            'backupCount': 2,
        }
    },
    'loggers': {
        'owf.enable.cef.object.access.logging': {
            'level': 'DEBUG',
            'handlers': ['console', 'event-file']
        },
        'owf.enable.cef.logging': {
            'level': 'DEBUG',
            'handlers': ['console', 'cef-file']
        },
        'django.security.DisallowedHost': {
            'handlers': ['console', ],
            'propagate': False,
            'level': 'ERROR',
        },
        # 'django.db.backends': {  # For SQL expressions
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        # },
    }
}

DEFAULT_USER_GROUP = 'OWF Users'
DEFAULT_ADMIN_GROUP = 'OWF Administrators'

# CAS
ENABLE_CAS = ast.literal_eval(os.getenv('OWF_ENABLE_CAS', 'False'))
if ENABLE_CAS:
    AUTHENTICATION_BACKENDS.append('django_cas_ng.backends.CASBackend')
    INSTALLED_APPS.append('django_cas_ng')

    CAS_EXTRA_LOGIN_PARAMS = ast.literal_eval(
        os.getenv('OWF_CAS_EXTRA_LOGIN_PARAMETERS', '{}')
    )
    CAS_RENAME_ATTRIBUTES = {
        os.getenv('OWF_CAS_USERNAME_ATTRIBUTE', 'uid'): 'username',
    }
    CAS_SERVER_URL = os.getenv('OWF_CAS_SERVER_URL')
    CAS_VERSION = os.getenv('OWF_CAS_VERSION', '2')

    CAS_CREATE_USER = False
    CAS_STORE_NEXT = True

# SSL (CAC)
ENABLE_SSL_AUTH = False
if ENABLE_SSL_AUTH:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    MIDDLEWARE += [
        'config.ssl_auth.SSLClientAuthMiddleware'
    ]

    AUTHENTICATION_BACKENDS += [
        'config.ssl_auth.SSLClientAuthBackend'
    ]

    AUTOCREATE_VALID_SSL_USERS = False
    EXTRACT_USERDATA_FN = 'config.ssl_auth.example.get_cac_id'
    USER_DN_SSL_HEADER = 'HTTP_X_SSL_USER_DN'

ENABLE_METRICS = False
METRICS_SERVER_URL = 'http://localhost:3000/metric'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1440 * 60

# REST CORS CONFIGURATION
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

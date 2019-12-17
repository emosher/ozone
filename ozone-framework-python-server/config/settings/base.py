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
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
CLIENT_DIR = os.path.join(ROOT_DIR, 'ozone-framework-client', 'packages', 'application')
CLIENT_BUILD_DIR = os.path.join(CLIENT_DIR, 'build')
WIDGETS_DIR = os.path.join(ROOT_DIR, 'ozone-example-widgets')
WIDGETS_BUILD_DIR = os.path.join(WIDGETS_DIR, 'build')
HELP_FILES = os.path.join(BASE_DIR, 'help_files')
HELP_FILES_URL = '/help_files/'

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
    'django_nose',
    'webpack_loader',

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

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--with-coverage',
    '--cover-html',
    '--cover-package=appconf,dashboards,domain_mappings,intents,legacy,metrics,owf_groups,people,preferences,'
    'roles,stacks,widgets',

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [CLIENT_BUILD_DIR, HELP_FILES, WIDGETS_BUILD_DIR]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['config/templates'],
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

LOGIN_URL = '/login.html'
LOGIN_REDIRECT_URL = '/index.html'

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

    CAS_CREATE_USER = ast.literal_eval(os.getenv('OWF_CAS_CREATE_USER', 'False'))
    CAS_STORE_NEXT = ast.literal_eval(os.getenv('OWF_CAS_STORE_NEXT', 'True'))

# SSL (CAC)
ENABLE_SSL_AUTH = ast.literal_eval(os.getenv('OWF_ENABLE_SSL_AUTH', 'False'))
if ENABLE_SSL_AUTH:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    MIDDLEWARE += [
        'config.ssl_auth.SSLClientAuthMiddleware'
    ]

    AUTHENTICATION_BACKENDS += [
        'config.ssl_auth.SSLClientAuthBackend'
    ]

    EXTRACT_USERDATA_FN = ast.literal_eval(os.getenv('OWF_EXTRACT_USERDATA_FN', 'config.ssl_auth.example.get_cac_id'))
    USER_DN_SSL_HEADER = ast.literal_eval(os.getenv('OWF_USER_DN_SSL_HEADER', 'HTTP_X_SSL_USER_DN'))
    USER_AUTH_STATUS_HEADER = ast.literal_eval(os.getenv('OWF_USER_AUTH_STATUS_HEADER', 'HTTP_X_SSL_AUTHENTICATED'))

ENABLE_METRICS = False
METRICS_SERVER_URL = 'http://localhost:3000/metric'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1440 * 60
SESSION_SAVE_EVERY_REQUEST = True


# REST CORS CONFIGURATION
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': '/',  # must end with slash
        'STATS_FILE': os.path.join(CLIENT_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
    }
}

ENABLE_CONSENT = True
CONSENT_TITLE = "DoD Privacy and Consent Notice"
CONSENT_MESSAGE = """\\
You are accessing a U.S. Government (USG) Information System (IS) that is provided for USG-authorized use \\
only. By using this IS (which includes any device attached to this IS), you consent to the following conditions:\\
\\n\\
\\n\\
* The USG routinely intercepts and monitors communications on this IS for purposes including, but not limited to, \\
penetration testing, COMSEC monitoring, network operations and defense, personnel misconduct (PM), law enforcement \\
(LE), and counterintelligence (CI) investigations.\\
\\n\\
* At any time, the USG may inspect and seize data stored on this IS.\\
\\n\\
* Communications using, or data stored on, this IS are not private, are subject to routine monitoring, interception, \\
and search, and may be disclosed or used for any USG-authorized purpose.\\
\\n\\
* This IS includes security measures (e.g., authentication and access controls) to protect USG interests--not for \\
your personal benefit or privacy.\\
\\n\\
* Notwithstanding the above, using this IS does not constitute consent to PM, LE or CI investigative searching or \\
monitoring of the content of privileged communications, or work product, related to personal representation or \\
services by attorneys, psychotherapists, or clergy, and their assistants. Such communications and work product are \\
private and confidential.\\
"""

ENABLE_USER_AGREEMENT = True
USER_AGREEMENT_TITLE = "User Agreement"
USER_AGREEMENT_MESSAGE = """\\
__STANDARD MANDATORY NOTICE AND CONSENT PROVISION__\\
\\n\\
\\n\\
By signing this document, you acknowledge and consent that when you access Department of Defense (DoD) information \\
systems:\\
\\n\\
\\n\\
You are accessing a U.S. Government (USG) information system (IS) (which includes any device attached to this \\
information system) that is provided for U.S. Government authorized use only. You consent to the following \\
conditions:\\
\\n\\
\\n\\
* The U.S. Government routinely intercepts and monitors communications on this information system for purposes \\
including, but not limited to, penetration testing, communications security (COMSEC) monitoring, network operations \\
and defense, personnel misconduct (PM), law enforcement (LE), and counterintelligence (CI) investigations.\\
\\n\\
* At any time, the U.S. Government may inspect and seize data stored on this information system.\\
\\n\\
* Communications using, or data stored on, this information system are not private, are subject to routine \\
monitoring, interception, and search, and may be disclosed or used for any U.S. Government-authorized purpose.\\
\\n\\
* This information system includes security measures (e.g., authentication and access controls) to protect U.S. \\
Government interests--not for your personal benefit or privacy.\\
\\n\\
* Notwithstanding the above, using an information system does not constitute consent to personnel misconduct, law \\
enforcement, or counterintelligence investigative searching or monitoring of the content of privileged communications \\
or data (including work product) that are related to personal representation or services by attorneys, \\
psychotherapists, or clergy, and their assistants. Under these circumstances, such communications and work products \\
are private and confidential, as further explained below:\\
\\n\\
  1. Nothing in this User Agreement shall be interpreted to limit the user's consent to, or in any other way restrict \\
or affect, any U.S. Government actions for purposes of network administration, operation, protection, or defense, or \\
for communications security. This includes all communications and data on an information system, regardless of any \\
applicable privilege or confidentiality.\\
\\n\\
  2. The user consents to interception/capture and seizure of ALL communications and data for any authorized purpose \\
(including personnel misconduct, law enforcement, or counterintelligence investigation). However, consent to \\
interception/capture or seizure of communications and data is not consent to the use of privileged communications or \\
data for personnel misconduct, law enforcement, or counterintelligence investigation against any party and does not \\
negate any applicable privilege or confidentiality that otherwise applies.\\
\\n\\
  3. Whether any particular communication or data qualifies for the protection of a privilege, or is covered by a \\
duty of confidentiality, is determined in accordance with established legal standards and DoD policy. Users are \\
strongly encouraged to seek personal legal counsel on such matters prior to using an information system if the user \\
intends to rely on the protections of a privilege or confidentiality.\\
\\n\\
  4. Users should take reasonable steps to identify such communications or data that the user asserts are protected \\
by any such privilege or confidentiality. However, the user's identification or assertion of a privilege or \\
confidentiality is not sufficient to create such protection where none exists under established legal standards and \\
DoD policy.\\
\\n\\
  5. A user's failure to take reasonable steps to identify such communications or data as privileged or confidential \\
does not waive the privilege or confidentiality if such protections otherwise exist under established legal standards \\
and DoD policy. However, in such cases the U.S. Government is authorized to take reasonable actions to identify such \\
communication or data as being subject to a privilege or confidentiality, and such actions do not negate any \\
applicable privilege or confidentiality.\\
\\n\\
  6. These conditions preserve the confidentiality of the communication or data, and the legal protections regarding \\
the use and disclosure of privileged information, and·thus such communications and data are private and confidential. \\
Further, the U.S. Government shall take all reasonable measures to protect the content of captured/seized privileged \\
communications and data to ensure they are appropriately protected.\\
\\n\\
* In cases when the user has consented to content searching or monitoring of communications or data for personnel \\
misconduct, law enforcement, or counterintelligence investigative searching, (i.e., for all communications and data \\
other than privileged communications or data that are related to personal representation or services by attorneys, \\
psychotherapists, or clergy, and their assistants), the U.S. Government may, solely at its discretion and in \\
accordance with DoD policy, elect to apply a privilege or other restriction on the U.S. Government's \\
otherwise-authorized use or disclosure of such information.\\
"""
SERVER_URL = "http://localhost:8000"

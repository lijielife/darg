# -*- coding: utf-8 -*-
"""
Django settings for darg project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import collections
import os
import sys

from kombu import Exchange, Queue

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _


def get_env_variable(var_name, fail_on_error=True):
    try:
        env_var = os.environ[var_name]
    except KeyError:
        if fail_on_error:
            raise ImproperlyConfigured("Set %s environment variable" % var_name)
        else:
            env_var = ''

    return env_var


VERSION = '0.6.24'

BASE_DIR = os.path.abspath(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SITE_ID = 1

ALLOWED_HOSTS = [
    'www.das-aktienregister.ch',
    ]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'django.contrib.flatpages',

    'registration',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'raven.contrib.django.raven_compat',
    'sorl.thumbnail',
    'djrill',
    'django_markdown',
    'markdownx',  # flatpage advanced admin
    'flatpage_meta',  # flatpage meta tags
    'reversion',
    'storages',
    'dbbackup',
    'django_celery_results',
    'django_celery_beat',
    'djstripe',

    # OTP
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',

    # -- zinnia
    'django_comments',
    'mptt',
    'tagging',
    'zinnia_bootstrap',
    'zinnia',
    # --

    'shareholder',
    'services',
    'company',
    'project',
    'reports',
    'utils',
    'pingen'
)

# just MIDDLEWARE in django 1.10
MIDDLEWARE_CLASSES = (
    'reversion.middleware.RevisionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'two_factor.middleware.threadlocals.ThreadLocals',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'company.middleware.CompanySubscriptionRequired'
)

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['project/templates'],  # required to load two factor tpls
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'project.context_processors.tracking',
                'zinnia.context_processors.version',
                'project.context_processors.default_protocol'
            ],
            'loaders': (
                'django.template.loaders.filesystem.Loader',
                'app_namespace.Loader',
                'django.template.loaders.app_directories.Loader',
            ),
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': ''
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'de-ch'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

THOUSAND_SEPARATOR = "'"

USE_THOUSAND_SEPARATOR = True

FORMAT_MODULE_PATH = [
    'formats',
]
# -- LOGGING

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'handlers': ['console', 'sentry'],
        'level': 'WARNING',
        'formatter': 'verbose',
    },
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                      '%(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler'
        },
        'test_logging_handler': {
            'level': 'DEBUG',
            'class': 'project.tests.helper.TestLoggingHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
        },
        'celery': {
            'level': 'WARNING',
            'handlers': ['sentry', 'console'],
            'propagate': False,
        },
        'selenium': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'easyprocess': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'shareholder': {
            'level': 'INFO',
            'handlers': ['console'],
        },
        'tests': {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    },
}

# -- CACHE
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# -- EMAIL
ADMINS = ()
SERVER_EMAIL = 'no-reply@das-aktienregister.ch'
EMAIL_SUBJECT_PREFIX = '[darg] '

MANAGERS = ADMINS + ()

# -- STATIC FILES
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    # os.path.join(BASE_DIR, 'static', 'minified'),
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'media', 'static')

MEDIA_ROOT = 'media'  # used also by zinnia for path inside static. is relative

MEDIA_URL = '/media/'

# --- SHAREHOLDERS APP
COMPANY_INITIAL_FIRST_NAME = u'Unternehmen'

# --- REGISTRATION
REGISTRATION_OPEN = True        # If True, users can register
ACCOUNT_ACTIVATION_DAYS = 7     # One-week activation window; you may, of cour
REGISTRATION_AUTO_LOGIN = True  # If True, the user will be automatically logg
LOGIN_REDIRECT_URL = '/start/'  # The page you want users to arrive at after t
LOGIN_URL = 'two_factor:login'  # The page users are directed to if they are n

# --- TWO FACTOR AUTH
TWO_FACTOR_PATCH_ADMIN = True
TWO_FACTOR_CALL_GATEWAY = 'two_factor.gateways.twilio.gateway.Twilio'
TWO_FACTOR_SMS_GATEWAY = 'two_factor.gateways.twilio.gateway.Twilio'
PHONENUMBER_DEFAULT_REGION = '+41'
TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''
TWILIO_CALLER_ID = ''

# --- REST
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGE_SIZE': 1000,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    # disable browsable api
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}
# angular does want this
APPEND_SLASH = False

# --- I18N
# add here for app module dirs to show up under 'project' filter in rosetta
LOCALE_PATHS = (
    # './i18n/locale/',
    # './shareholder/locale/',
    # './services/locale/',
    os.path.join(BASE_DIR, 'i18n', 'locale'),
    os.path.join(BASE_DIR, 'shareholder', 'locale'),
    os.path.join(BASE_DIR, 'services', 'locale'),
    os.path.join(BASE_DIR, 'reports', 'locale'),
)

# --- Sentry
RAVEN_CONFIG = {
    'dsn': '',
}

# -- TEST RUNNEr
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# -- TRACKING
TRACKING_ENABLED = not DEBUG
TRACKING_CODE = ""

# -- BLOG
ZINNIA_UPLOAD_TO = os.path.join(MEDIA_ROOT, 'blog')
ZINNIA_MARKUP_LANGUAGE = 'markdown'

# -- SENDFILE for downloads
SENDFILE_BACKEND = 'sendfile.backends.nginx'
SENDFILE_ROOT = os.path.join(MEDIA_ROOT, 'private')
SENDFILE_URL = "/media/private"

MANDRILL_API_KEY = "<your Mandrill key>"
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
DEFAULT_FROM_EMAIL = "info@das-aktienregister.ch"
MANDRILL_SETTINGS = {
    'tracking_domain': 'mail.das-aktienregister.ch',
    'track_opens': True,
}
MANDRILL_SHAREHOLDER_STATEMENT_TEMPLATE = None
MANDRILL_API_BASE_URL = 'https://mandrillapp.com/api/1.0/'

# --- CELERY
# CELERY_ALWAYS_EAGER = False # use default anyway
CELERYD_HIJACK_ROOT_LOGGER = False
CELERY_DEFAULT_QUEUE = 'darg'
CELERY_QUEUES = (
    Queue('darg', Exchange('darg'), routing_key='darg'),
)
CELERY_RESULT_BACKEND = 'django-db'
BROKER_URL = 'amqp://darg:darg@localhost:5672/darg'

# --- MARKDOWN X

MARKDOWNX_MARKDOWNIFY_FUNCTION = 'markdownx.utils.markdownify'
MARKDOWNX_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.nl2br',
    'markdown.extensions.smarty',
]
# crispy images pls
MARKDOWNX_IMAGE_MAX_SIZE = {'size': (900, 900), 'quality': 100}

# Media path
# Path, where images will be stored in MEDIA_ROOT folder
MARKDOWNX_MEDIA_PATH = 'f/'

# TESTING
TEST_ERROR_SEND_EMAIL = bool(
    os.environ.get('DJANGO_TEST_ERROR_SEND_EMAIL', True))
TEST_ERROR_FROM_EMAIL = 'no-reply@das-aktienregister.ch'
TEST_ERROR_EMAIL_RECIPIENTS = os.environ.get(
    'DJANGO_TEST_ERROR_EMAIL_RECIPIENTS',
    'jirka.schaefer@tschitschereengreen.com').split(',')
TEST_ERROR_KEEP_SCREENSHOTS = bool(os.environ.get(
    'DJANGO_TEST_ERROR_KEEP_SCREENSHOTS', False))
TEST_ERROR_SCREENSHOTS_DIR = '.'
TEST_WEBDRIVER_IMPLICIT_WAIT = 10
TEST_WEBDRIVER_WAIT_TIMEOUT = 10
TEST_WEBDRIVER_PAGE_LOAD_TIMEOUT = 5

# chromedriver
TEST_CHROMEDRIVER_EXECUTABLE = os.environ.get(
    'DJANGO_TEST_CHROMEDRIVER_EXECUTABLE', './chromedriver')

# THUMBS
THUMBNAIL_PRESERVE_FORMAT = True

# django-dbbackup
DROPBOX_ROOT_PATH = get_env_variable('DROPBOX_ROOT_PATH', fail_on_error=False)

if DROPBOX_ROOT_PATH:
    DBBACKUP_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
    DBBACKUP_STORAGE_OPTIONS = {
        'oauth2_access_token': get_env_variable('DROPBOX_ACCESS_TOKEN'),
    }

# swiss bank list download url
SWISS_BANKS_DOWNLOAD_URL = ('https://www.six-interbank-clearing.com/dam'
                            '/downloads/bc-bank-master/bcbankenstamm')


# app internal settings
DISPO_SHAREHOLDER_NUMBER = 'DISPO-1'


# need to differentiate instances
def backup_filename(databasename, servername, datetime, extension,
                    content_type):
    import getpass
    username = getpass.getuser()
    return ('{username}-{databasename}-{servername}-{datetime}.{extension}'
            ''.format(
                **{'username': username, 'databasename': databasename,
                   'servername': servername, 'datetime': datetime,
                   'extension': extension})
            )


def media_backup_filename(databasename, servername, datetime, extension,
                          content_type):
    import getpass
    username = getpass.getuser()
    return '{username}-mediafiles-{servername}-{datetime}.{extension}'.format(
        **{'username': username, 'servername': servername,
           'datetime': datetime, 'extension': extension})

DBBACKUP_FILENAME_TEMPLATE = backup_filename
DBBACKUP_MEDIA_FILENAME_TEMPLATE = media_backup_filename


# SHAREHOLDER STATEMENT
SHAREHOLDER_STATEMENT_ROOT = os.path.join(
    SENDFILE_ROOT, 'shareholder', 'statements')
# send notify to operators that statements will be generated
SHAREHOLDER_STATEMENT_OPERATOR_NOTIFY_DAYS = 7
# days to watch if email was opened
SHAREHOLDER_STATEMENT_EMAIL_OPENED_DAYS = 7
# send notify to operators that statement were generated
SHAREHOLDER_STATEMENT_REPORT_OPERATOR_NOTIFY_DAYS = 14

# PINGEN API
PINGEN_API_TOKEN = None  # set this in local settings
PINGEN_SEND_ON_UPLOAD = False  # careful here!
PINGEN_SEND_COLOR = 2
PINGEN_API_URL = 'https://api.pingen.com'  # can't upload to stage api!
# see pingen/conf.py for more options

# stripe
STRIPE_PUBLIC_KEY = get_env_variable('STRIPE_PUBLIC_KEY', fail_on_error=False)
STRIPE_SECRET_KEY = get_env_variable('STRIPE_SECRET_KEY', fail_on_error=False)
DJSTRIPE_WEBHOOK_URL = r"^_stripe/webhooks/$"
DJSTRIPE_INVOICE_FROM_EMAIL = DEFAULT_FROM_EMAIL
DJSTRIPE_SUBSCRIBER_MODEL = 'shareholder.Company'
DJSTRIPE_CURRENCIES = (('chf', _('Swiss franc'),),)
DJSTRIPE_PLANS = collections.OrderedDict((
    ('startup', {
        'stripe_plan_id': 'startup',
        'name': _('StartUp'),
        'description': _(u'Designed für StartUps und Neugründungen'),
        'price': 0,
        'currency': 'chf',
        'interval': 'month',
        'features': {
            'shareholders': {
                'max': 20,
                'validators': {
                    'create': [
                        'company.validators.features.ShareholderCreateMaxCountValidator'
                    ]
                }
            },
            'positions': {},
            'options': {},
            'securities': {
                'max': 1,
                'validators': {
                    'create': [
                        'company.validators.features.SecurityCreateMaxCountValidator'
                    ]
                }
            },
            'shares': {},
            'gafi': {},
            'revision': {}
        },
        'validators': [
            'company.validators.features.ShareholderCountPlanValidator',
            'company.validators.features.SecurityCountPlanValidator'
        ]
    }),
    ('professional', {
        'stripe_plan_id': 'professional',
        'name': _('Professional'),
        'description': _(u'Für etablierte Aktiengesellschaften und KMU'),
        'price': 1799,  # 17.99
        'currency': 'chf',
        'interval': 'month',
        'features': {
            'shareholders': {
                'price': 49,  # 0.49
                'validators': {
                    'create': []
                }
            },
            'positions': {},
            'options': {},
            'securities': {
                'price': 1500,  # 15.00 CHF per month
                'validators': {
                    'create': []
                }
            },
            'shares': {},
            'gafi': {},
            'revision': {},
            'shareholder_statements': {},
            'numbered_shares': {},
            'email_support': {}
        },
        'validators': []
    }),
    ('enterprise', {
        'stripe_plan_id': 'enterprise',
        'name': _('Enterprise'),
        'description': _(
            u'First-Class-Service für grosse Aktionärsgesellschaften'),
        'price': 17900,  # 179.00
        'currency': 'chf',
        'interval': 'month',
        'features': {
            'shareholders': {
                'price': 9,  # 0.09
                'validators': {
                    'create': []
                }
            },
            'positions': {},
            'options': {},
            'securities': {
                'price': 1500,  # 15.00 CHF per month
                'validators': {
                    'create': []
                }
            },
            'shares': {},
            'gafi': {},
            'revision': {},
            'shareholder_statements': {},
            'numbered_shares': {},
            'email_support': {},
            'shareholder_admin_pro': {},
            'premium_support': {},
            'custom_export_import': {}
        },
        'validators': []
    })
))

from utils.subscriptions import stripe_subscriber_request_callback  # noqa
DJSTRIPE_SUBSCRIBER_MODEL_REQUEST_CALLBACK = stripe_subscriber_request_callback

# all available subscription features
SUBSCRIPTION_FEATURES = collections.OrderedDict((
    ('shareholders', {'title': _('Shareholders'), 'core': True}),
    ('positions', {'title': _('Positions'), 'core': True}),
    ('options', {'title': _('Options'), 'core': True}),
    ('securities', {'title': _('Securities'), 'core': True}),
    ('shares', {
        'title': _(u'Aktienausgabe, Aktienkauf, -verkauf, '
                   u'Kapitalerhöhung, Aktiensplit')
    }),
    ('gafi', {'title': _('GAFI Validierung')}),
    ('revision', {'title': _('Revisionssicherheit')}),
    ('shareholder_statements', {
        'title': _('Depotauszug Email & Brief'),
        'annotation': _('Es entstehen weitere Kosten bei Briefversand '
                        'pro versendetem Brief.'),
        'form_fields': [
            'is_statement_sending_enabled',
            'statement_sending_date'
        ]
    }),
    ('numbered_shares', {'title': _('Nummerierte Aktien')}),
    ('email_support', {'title': _('Email Support')}),
    ('shareholder_admin_pro', {'title': _(u'Profi-Verwaltung Aktionäre')}),
    ('premium_support', {'title': _('Premium-Support 24/7')}),
    ('custom_export_import', {'title': _('Custom Export/Import')})
))

DEFAULT_HTTP_PROTOCOL = 'https'  # used by djstripe when sending emails

COMPANY_INVOICES_ROOT = os.path.join(SENDFILE_ROOT, 'company', 'invoices')
# NOTE: invoice id will be added to invoice filename
COMPANY_INVOICE_FILENAME = u'das-aktienregister-rechnung'
# whether to include VAT in company (pdf) invoices or not
COMPANY_INVOICE_INCLUDE_VAT = False
COMPANY_INVOICE_VAT = 19  # in percent
# NOTE: set this to True to include all invoice items directly into the invoice
#       email. If not set, the items will only we included, if pdf invoice is
#       missing. If this is set to False, items will never be included in email
# COMPANY_INVOICE_INCLUDE_IN_EMAIL = True

INVOICE_FROM_ADDRESS = [
    'KKD Komm. GmbH',
    'Pulsnitzer Str. 52',
    '01936 Grossnaundorf',
    'Deutschland'
]


if 'test' in sys.argv:
    try:
        from .tests import *  # noqa
    except ImportError:
        pass


try:
    from project.settings.local import *  # noqa
except ImportError:
    # print "no local conf"
    pass

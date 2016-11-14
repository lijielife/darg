from .base import *
import os

DEBUG = True

MANAGERS = ADMINS

SESSION_COOKIE_NAME = 'darg-sessionid'

TRACKING_ENABLED = True
TRACKING_CODE = 'UA-58468401-4'  # used by test

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
# for local dev use this...
# NOSE_ARGS = ['--pdb', '-s', '--logging-level=WARNING']
NOSE_ARGS = ['--nologcapture', '--with-enhanced-descriptions']

INSTALLED_APPS = INSTALLED_APPS + ('rosetta', 'django_nose',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# -- SENDFILE for downloads
SENDFILE_BACKEND = 'sendfile.backends.development'

INSTAPAGE_TOKEN = get_env_variable('INSTAPAGE_TOKEN')
INSTAPAGE_ACCESS_TOKEN = get_env_variable('INSTAPAGE_ACCESS_TOKEN')
INSTPAGE_ENABLED = True

CELERY_ALWAYS_EAGER = True

# -- RAVEN
RAVEN_CONFIG = {
    'dsn': get_env_variable('RAVEN_DSN'),
    'dsn_public': get_env_variable('RAVEN_DSN_PUBLIC'),
}

try:
    from .dev_local import *
except ImportError:
    pass

import os
import os.path
import sys

PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])
APPSERVER = os.uname()[1]

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, 'sqlite.db'),
    }
}

LOGIN_URL = "/andy/accounts/login/"

LOGIN_REDIRECT_URL = "/andy/softball/"

USE_X_FORWARDED_HOST = True
TIME_ZONE = 'UTC'
SITE_ID = 1
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True
APPEND_SLASH = True

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static-collected')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY='KHN0ZGluKT0gYzI2MjI3OTBlZGY3OGZmOTU0N2YyNWI1YjE2MD'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (os.path.join(PROJECT_PATH, 'templates'),)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

MESSAGE_STORAGE = (
    'django.contrib.messages.storage.session.SessionStorage'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'project',
    'softball',
    'django.contrib.messages',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG', 'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG', 'class':'logging.StreamHandler', 'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR', 'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers':['console'], 'level':'DEBUG', 'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'], 'level': 'ERROR', 'propagate': False,
        },
    }
}

MANDRILL_API_KEY = 'acefe6c5-538b-4851-a743-f70f849b1ef6'

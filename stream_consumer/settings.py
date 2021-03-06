# Django settings for stream_consumer project.

# heroku config:set ADN_CLIENT_ID=<Your Client ID>
# heroku config:set ADN_CLIENT_SECRET=<Your Client Secret>
import os

ADN_CLIENT_ID = os.environ['ADN_CLIENT_ID']
ADN_CLIENT_SECRET = os.environ['ADN_CLIENT_SECRET']
ADN_APP_TOKEN = os.environ.get('ADN_APP_TOKEN')
ADN_USER_ACCESS_TOKEN = os.environ.get('ADN_USER_ACCESS_TOKEN')

ADN_FILTER_SCHEMA = {
    'clauses': [
        {
            'field': u'/data/entities/mentions/*/id',
            'object_type': u'post',
            'operator': 'one_of',
            'value': u'$authorized_userids'
        }, {
            'field': u'/data/follows_user/id',
            'object_type': u'user_follow',
            'operator': 'one_of',
            'value': u'$authorized_userids'
        }, {
            'field': u'/data/post/user/id',
            'object_type': u'star',
            'operator': 'one_of',
            'value': u'$authorized_userids'
        }, {
            'field': u'/data/repost_of/user/id',
            'object_type': u'post',
            'operator': 'one_of',
            'value': u'$authorized_userids'
        }, {
            'field': u'/data/user/id',
            'object_type': u'mute',
            'operator': 'one_of',
            'value': u'$authorized_userids'
        }, {
            'field': u'/meta/channel_type',
            'object_type': u'message',
            'operator': 'equals',
            'value': u'net.app.core.pm'
        }, {
            'field': u'/meta/channel_type',
            'object_type': u'message',
            'operator': 'equals',
            'value': u'net.app.core.broadcast'
        }
    ],
    'match_policy': 'include_any',
    'name': u'my_users_actions',
}

ADN_STREAM_SCHEMA = {
    "object_types": [
        "star",
        "user_follow",
        "message",
        "channel",
    ],
    "type": "long_poll",
    "key": os.environ.get('ADN_STREAM_NAME', 'my_users_actions_dev')
}

ADN_STREAM_FILTER_ID = os.environ.get('ADN_STREAM_FILTER_ID')


GCM_CLIENT_ID = os.environ.get('GCM_CLIENT_ID')
GCM_CLIENT_SECRET = os.environ.get('GCM_CLIENT_SECRET')
GCM_REFRESH_TOKEN = os.environ.get('GCM_REFRESH_TOKEN')

VALID_MESSAGE_PREFERENCES = [
    'pm',
    'alert',
    'mention',
    'repost',
    'star',
    'user_follow',
] 

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '9niux_h5r*!x&hfm&c!e=8*+r9jr--xypped^le6#bz7qkg!c!'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'users.middleware.ADNTokenAuthMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'stream_consumer.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'stream_consumer.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stream_consumer',
    'notifications',
    'users',
    'gunicorn',
    'corsheaders',
    'django.contrib.admin',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        '*': {
            'handlers': ['console'],
            'propagate': True,
        }
    }
}

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {}
if dj_database_url.config():
    DATABASES['default'] =  dj_database_url.config()
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': './database.db',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': '',
            'PASSWORD': '',
            'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '',                      # Set to empty string for default.
        }
    }
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

CORS_ORIGIN_ALLOW_ALL = True

def get_cache():
  import os
  try:
    os.environ['MEMCACHE_SERVERS'] = os.environ['MEMCACHIER_SERVERS'].replace(',', ';')
    os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHIER_USERNAME']
    os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHIER_PASSWORD']
    return {
      'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'TIMEOUT': 500,
        'BINARY': True,
        'OPTIONS': { 'tcp_nodelay': True }
      }
    }
  except:
    return {
      'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
      }
    }

CACHES = get_cache()

import os
import sys
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "/www/django_lib/BeautifulSoup-3.0.8"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "/www/django_lib/dcramer-django-sphinx-b8f1943"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "/www/vhosts/dizcollect.com/html"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "/www/django_lib/feedparser-4.1"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "/www/django_lib"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "/www/django_lib/sorl-thumbnail-3.2.5"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "/www/django_lib/elementtree-1.2.6-20050316"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "/www/django_lib/boto-1.9b"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "/www/django_lib/python2.5"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "/usr/local/lib/python2.5"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "/usr/local/lib/python2.5/site-packages/PIL"))
os.environ['TZ'] = 'US/Pacific'

DEBUG = False
#DEBUG = True
#TEMPLATE_DEBUG = DEBUG
#THUMBNAIL_DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'dizcollect'             # Or path to database file if using sqlite3.
DATABASE_USER = 'dizcollect'             # Not used with sqlite3.
DATABASE_PASSWORD = 'ENV_PASS'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los Angles'

# Timezoneused by pytz lib
TZ = 'US/Pacific'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/www/vhosts/media.dizcollect.com/html/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://media.dizcollect.com/'


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ew!l*9fdb5f8mk3^)rj*j@0!ghfq=e-3+ac+r30%_q=*!kyn#q'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
        "django.core.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.request",
        "context_processors.settings",
)

AUTHENTICATION_BACKENDS = (
    'facebookconnect.models.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'facebook.djangofb.FacebookMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'facebookconnect.middleware.FacebookConnectMiddleware',
    'pagination.pagination.middleware.PaginationMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	"/www/vhosts/dizcollect.com/html/templates",
	"/www/django_lib/ursula/templates",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'facebook',
    'facebookconnect',                  #facebook connect
    'ursula',                           #our collection app
    'pagination.pagination',            #pagination
    'sorl.thumbnail',                   #thumbnail creation
    'elementtree',                      #xml parsing lib, overrides built in django with new functions
    'djangosphinx',
    'registration',                     #registration
    'template_utils',
)

# Static URL
STATIC_URL = "http://static.dizcollect.com"


# Sphinx 0.9.8
SPHINX_API_VERSION = 0x116
SPHINX_SERVER = 'localhost'
SPHINX_PORT = 3312

# Pagination
PAGINATION_DEFAULT_WINDOW = 5

# Akismet API Key
AKISMET_API_KEY = 'a0325929c3fd'

# sorl thumbnail settings
THUMBNAIL_SUBDIR = '_adjusted'

APPEND_SLASH = True

# registration settings
ACCOUNT_ACTIVATION_DAYS = 7

# Email Settings
EMAIL_HOST='mail.aidanslair.com'
EMAIL_HOST_USER='stb@dizcollect.com'
EMAIL_HOST_PASSWORD='PASS_HERE'
EMAIL_USE_TLS = True
EMAIL_PORT='25'
DEFAULT_FROM_EMAIL = 'registration@dizcollect.com'
SERVER_EMAIL = "stb@dizcollect.com"
CONTACT_EMAIL = "stb@dizcollect.com"


## Amazon Settings
AWS_ACCESS_KEY_ID = 'AMAZON_KEY'
AWS_ASSOCIATE_TAG = 'dizcollect-20'
AWS_SECRET_ACCESS_KEY = 'AMAZON_SHARED_SECRET'
AFFILIATE_ID = "dizcollect-20"

# Facebook Config
FACEBOOK_CACHE_TIMEOUT = 1800
FACEBOOK_API_KEY= 'FB_KEY'
FACEBOOK_SECRET_KEY= 'FB_SECRET'
FACEBOOK_INTERNAL = True
LOGIN_REDIRECT_URL = '/'

DUMMY_FACEBOOK_INFO = {
    'uid':0,
    'name':'(Private)',
    'first_name':'(Private)',
    'pic_square_with_logo':'/public/images/t_silhouette.jpg',
    'affiliations':None,
    'status':None,
    'proxied_email':None,
}

THUMBNAIL_QUALITY = 95



# Memcache
#CACHE_BACKEND = "memcached://127.0.0.1:191419/"
#CACHE_MIDDLEWARE_SECONDS = 5000

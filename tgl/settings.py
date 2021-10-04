import os
from pathlib import Path
from django.contrib.messages import constants as messages
import sentry_sdk
import ast
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'payments.apps.PaymentsConfig',
    'accounts.apps.AccountsConfig',
    'main.apps.MainConfig',
    'announcements.apps.AnnouncementsConfig',

    'django_admin_listfilter_dropdown',
    'localflavor',
    "post_office",
    'compressor',

]

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.cache.FetchFromCacheMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
]

ROOT_URLCONF = 'tgl.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'tgl.wsgi.application'

dotenv_file = BASE_DIR / ".env"
if os.path.isfile(dotenv_file):
    import dotenv
    dotenv.load_dotenv(dotenv_file)

    PRODUCTION_SERVER = False
    DEBUG = True
    SECRET_KEY = '7$xw$^&2rne%#gqm!-n!y$%!7*uahe1cmnc!8hd3j+=syy3=$)'
    LOCAL = True
else:
    LOCAL = ast.literal_eval(os.environ.get('LOCAL','False'))
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    ADMINS = [('dhruva', os.environ['EMAIL_HOST_USER'])]

    PRODUCTION_SERVER = True
    DEBUG = ast.literal_eval(os.environ.get('DEBUG', 'False'))
    SECRET_KEY = os.environ.get('SECRET_KEY','SECRET_KEY')
    
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    

if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES = {'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


sentry_sdk.init(
    dsn=os.environ.get('SENTRY_URL'),
    integrations=[DjangoIntegration(), RedisIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

if not os.getenv('WHITENOISE'):
    MIDDLEWARE = [MIDDLEWARE[0]] + \
        ['whitenoise.middleware.WhiteNoiseMiddleware']+MIDDLEWARE[1:]
    INSTALLED_APPS = INSTALLED_APPS[0:-1] + \
        ['whitenoise.runserver_nostatic',]+[INSTALLED_APPS[-1]]

INSTAMOJO_AUTH_KEY = os.environ.get('INSTAMOJO_AUTH_KEY')
INSTAMOJO_PRIVATE_TOKEN = os.environ.get('INSTAMOJO_PRIVATE_TOKEN')


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

LANGUAGE_CODE = 'en-us'

CELERY_TIMEZONE = TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATIC_URL = '/static/'
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]


MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

WHITENOISE_MAX_AGE = 9000
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = []

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


PASSWORD_RESET_TIMEOUT_DAYS = 1


#Overiding a message tag
MESSAGE_TAGS = {
    messages.ERROR : 'danger'
}

# # Deployment check
if PRODUCTION_SERVER:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000 
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "same-origin"
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CACHES = {
        'default': {
            'BACKEND': 'django_bmemcached.memcached.BMemcached',
            'LOCATION': os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','),
            'OPTIONS': {
                'username': os.environ.get('MEMCACHEDCLOUD_USERNAME'),
                'password': os.environ.get('MEMCACHEDCLOUD_PASSWORD')
            }
        }
    }

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

COMPRESS_ENABLED = ast.literal_eval(os.environ.get('COMPRESS_ENABLED', 'True'))
COMPRESS_OFFLINE = ast.literal_eval(os.environ.get('COMPRESS_OFFLINE', 'True'))
COMPRESS_PRECOMPILERS = (
    ('text/x-sass', 'django_libsass.SassCompiler'),
    ('text/x-scss', 'django_libsass.SassCompiler'),
)
COMPRESS_CSS_HASHING_METHOD = 'content'
COMPRESS_FILTERS = {
    'css': [
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.rCSSMinFilter',
    ],
    'js': [
        'compressor.filters.jsmin.JSMinFilter',
    ]
}
HTML_MINIFY = True
KEEP_COMMENTS_ON_MINIFYING = False
DJANGO_ALLOW_ASYNC_UNSAFE = True

USE_THOUSAND_SEPARATOR = True

SESSION_COOKIE_AGE = 1 * 60 * 60

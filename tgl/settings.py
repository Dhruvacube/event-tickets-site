import os
from pathlib import Path
from django.contrib.messages import constants as messages


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
    'user.apps.UserConfig',
    'main.apps.MainConfig',
    
    'localflavor',
    "post_office",

]

AUTH_USER_MODEL = 'user.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
else:    
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

if not os.getenv('WHITENOISE'):
    MIDDLEWARE = [MIDDLEWARE[0]] + \
        ['whitenoise.middleware.WhiteNoiseMiddleware']+MIDDLEWARE[1:]
    INSTALLED_APPS = INSTALLED_APPS[0:-1] + \
        ['whitenoise.runserver_nostatic',]+[INSTALLED_APPS[-1]]


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

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATIC_URL = '/static/'


MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'


LOGIN_REDIRECT_URL = 'view_profile'
# LOGOUT_REDIRECT_URL = 'home'
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

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

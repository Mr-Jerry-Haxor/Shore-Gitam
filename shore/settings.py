from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = str(os.getenv('SECRET_KEY'))

DEVELOPMENT = os.getenv('DEVELOPMENT') == 'True'

if DEVELOPMENT:
    DEBUG = True
    ALLOWED_HOSTS = ["*"]
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DEBUG = False
    ALLOWED_HOSTS = ['shore.gitam.edu', '127.0.0.1']
    DATABASES = {
        'default': {
            'ATOMIC_REQUESTS': False,
            'AUTOCOMMIT': True,
            'CONN_MAX_AGE': 0,
            'ENGINE': 'django.db.backends.mysql',
            'NAME': str(os.getenv('DB_NAME')),
            'USER': str(os.getenv('DB_USER')),
            'PASSWORD': str(os.getenv('DB_PASSWORD')),
            'HOST': str(os.getenv('DB_HOST')),
            'PORT' : str(os.getenv('DB_PORT')),
        }
    }

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'social_django',
    'import_export',
    'coreteam',
    'comingsoon',
    'shore23',
    'hospitality',
    'prelims',
    'promotion',
    'payments',
    'events',
    'festpass',
    'sports',
    'ngusers',
    'teams',
    'security',
    'timeline',
    "production_admin",
    "home",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # custom context processor for retrieveing dates from meal model
                'hospitality.context_processors.formatted_dates',
                
                # Add the following two
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'shore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_COOKIE_AGE = 60 * 60 * 4

CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000','https://shore.gitam.edu']

AUTH_USER_MODEL = 'coreteam.CustomUser' 

AUTHENTICATION_BACKENDS = [
  'social_core.backends.google.GoogleOAuth2',
  'django.contrib.auth.backends.ModelBackend',
]



LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'homepage'


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = str(os.getenv('GOOGLE_KEY'))
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = str(os.getenv('GOOGLE_SECRET'))


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = str(os.getenv('MAILID'))
EMAIL_HOST_PASSWORD = str(os.getenv('MAILPASSWORD'))
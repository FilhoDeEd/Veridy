import os

from enum import StrEnum
from pathlib import Path


class Envs(StrEnum):
    PRODUCTION = 'production'
    STAGING = 'staging'
    DEVELOPMENT = 'development'


def get_secret(key: str, default: str = '') -> str:
    value = os.getenv(key, default)
    if os.path.isfile(value):
        with open(value) as f:
            return f.read()
    return value


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-n+kcttfsm2zl2$83_^+-@2ui9)=03&f38a^(m4qcq*0-bf3+__'


AUTH_USER_MODEL = 'common.VeridyUser'


DEBUG = True


ALLOWED_HOSTS = ['.localhost', '127.0.0.1', '[::1]']


STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = '/home/edson/media/'  # Temporário enquanto não tem Docker


AUTHENTICATION_BACKENDS = [
    'common.backends.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend'
]


DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

PROJECT_APPS = [
    'common',
    'document',
    'institution',
    'subject'
]

THIRDPARTY_APPS = [
    'crispy_forms',
    'crispy_bootstrap5'
]

INSTALLED_APPS = DEFAULT_APPS + PROJECT_APPS + THIRDPARTY_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'core.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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


LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True


LOGIN_URL = "/auth/login/"
LOGOUT_URL = "/auth/logout/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/auth/login/"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

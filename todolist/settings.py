from pathlib import Path

from envparse import env

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR.joinpath('.env')

if ENV_PATH.is_file():
    env.read_envfile(ENV_PATH)

SECRET_KEY = env('SECRET_KEY')

DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'social_django',
    'core',
    'goals',
]

if DEBUG:
    INSTALLED_APPS += [
        'django_extensions',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'todolist.urls'

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

WSGI_APPLICATION = 'todolist.wsgi.application'

AUTH_USER_MODEL = 'core.User'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST', default='127.0.0.1'),
        'PORT': env('POSTGRES_PORT', default='5432'),
    }
}

REST_FRAMEWORK = {
    # 'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}


# OpenAPI settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Todolist API',
    'DESCRIPTION': 'This is an API for Todolist application',
    'VERSION': '1.0.0'
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

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)



LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR.joinpath('static')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_VK_OAUTH2_KEY = env.str('VK_OAUTH2_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = env.str('VK_OAUTH_SECRET')
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/logged-in/'
SOCIAL_AUTH_USER_MODEL = 'core.User'
SOCIAL_AUTH_vk_OAUTH2_SCOPE = ['email']
AUTHENTICATION_BACKENDS = (
    'social_core.backends.vk.VKOAuth2',
    'django_contrib.auth.backends.ModelBackend',
)

"""
Django settings for gopython3 project.

For more information on this file, see
https://docs.djangoproject.com/en//topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en//ref/settings/
"""
import os

from configurations import Configuration, values


class Common(Configuration):

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = values.PathValue(os.path.dirname(os.path.dirname(__file__)))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en//howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '8t5=#r0m*^9b3!fab+b3($*ky@@v#c8)g10ey&krrt3uwd1*+d'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    TEMPLATE_DEBUG = True

    ALLOWED_HOSTS = []

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'frontend'
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = 'gopython3.urls'

    WSGI_APPLICATION = 'gopython3.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en//ref/settings/#databases
    # http://django-configurations.readthedocs.org/en/latest/values/#configurations.values.DatabaseURLValue

    DATABASES = values.DatabaseURLValue('sqlite://%s' % os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3'), environ=True)

    # Internationalization
    # https://docs.djangoproject.com/en//topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en//howto/static-files/

    STATIC_URL = '/static/'


class Dev(Common):
    """
    The in-development settings and the default configuration.
    """
    pass


class Prod(Common):
    """
    The in-production settings.
    """
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG

    SECRET_KEY = values.SecretValue()

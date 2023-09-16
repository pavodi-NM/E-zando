
import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django_countries.base import _

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = []
AUTH_USER_MODEL = 'StandardApps.User'


# Application definition

INSTALLED_APPS = [
    'decorators',
    'StandardApps',
    'Account',
    'Checkout',
    'Dashboard',
    'Shop',
    'chat',
    'Home',
    'Help',
    'StandardApps.templatetags',
    'templates.accounts',
    'templates.vendor-dashboard',
    'templates.chatroom',
    'global_scripts',
    'django_countries',
    'crispy_forms',
    'mptt',
    'django_filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'paypalcheckoutsdk',
    'responsive',
    # for chatroom
    'channels',
    # The following apps are required for django allauth:

    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

    'sslserver',

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
# For django responsive devices
MIDDLEWARE_CLASSES = (

    'responsive.middleware.ResponsiveMiddleware'

)
# For django responsive devices


ROOT_URLCONF = 'eCommerceBilMarket.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # make the view available in all pages of the website
                'global_scripts.context_processors.categories',
                'global_scripts.context_processors.subcategories',
                'global_scripts.context_processors.categorieswithchildren',
                'global_scripts.context_processors.wish_list_total',
                'global_scripts.context_processors.user_total_orders',
                'Dashboard.views.prodcount',
                'global_scripts.context_processors.carts',
                'global_scripts.context_processors.vendeur',
                'global_scripts.context_processors.vendeurbusiness',
                'global_scripts.context_processors.totalsale',
                'global_scripts.context_processors.special_products',
                # anonymous user
                'global_scripts.context_processors.anonymous_user_cart',
                'global_scripts.context_processors.sub_categories_only',
                # for django responsive 2, to manage screen size and content
                'responsive.context_processors.device',
            ],
        },
    },
]

WSGI_APPLICATION = 'eCommerceBilMarket.wsgi.application'
ASGI_APPLICATION = "eCommerceBilMarket.asgi.application"

# User redis later for deployment, check celerry series in very academic (how to utilize redis on externalserver)


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bilocost',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


#VENDOR_LOGIN_REDIRECT_URL = 'vendor-enregistrement/'

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# Including css files

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Indispensable for image display
# STATIC_ROOT = BASE_DIR / 'static_cdn'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Django allauth dependencies
AUTHENTICATION_BACKENDS = [

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

]

# This is for my custom forms
ACCOUNT_FORMS = {
    'change_password': 'Account.forms.MyCustomChangePasswordForm',
    'reset_password': 'Account.forms.MyCustomResetPasswordForm'
}

# This is for social adapter
ACCOUNT_ADAPTER = 'Account.my_account_adapter.MyAccountAdapter'

# This is for local email confirmation
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SITE_ID = 1
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

LOGIN_URL = '/accounts/signin/client/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = LOGIN_REDIRECT_URL
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# this will help the user to sign either with their email or username
ACCOUNT_AUTHENTICATION_METHOD = "username_email"

# Account login attempts and timeout
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 3
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
# Account user remember
#TODO: LATER
ACCOUNT_SESSION_REMEMBER = None
# email uniqueness
ACCOUNT_UNIQUE_EMAIL = True
# Social account provider for google
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name'
        ],
        'EXCHANGE_TOKEN': True,
        # 'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v7.0',
    }

}
# Social account provider for facebook


RESPONSIVE_MEDIA_QUERIES = {
    'smallern': {
        'verbose_name': _('Small screens'),
        'min_width': 520,
        'max_width': 1120,
    },
    'medium': {
        'verbose_name': _('Medium screens'),
        'min_width': 641,
        'max_width': 1024,
    },
    'large': {
        'verbose_name': _('Large screens'),
        'min_width': 1025,
        'max_width': 1440,
    },
    'xlarge': {
        'verbose_name': _('XLarge screens'),
        'min_width': 1441,
        'max_width': 1920,
    },
    'xxlarge': {
        'verbose_name': _('XXLarge screens'),
        'min_width': 1921,
        'max_width': None,
    }
}

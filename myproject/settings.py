"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import platform
import os
from myproject.redirect_middleware import LoginRequiredMiddleware
from myproject.middleware import AutoLogoutMiddleware
import socket

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-a^-!si_9u(5noyi=)l%uno@o!0kn95cba#2ajn)2lwdmi^^%e&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['*']

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'flat_responsive', # only if django version < 2.0
    'flat', # only if django version < 1.9
    'colorfield',
    'admin_menu',
    'axes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'crispy_forms',
    'crispy_bootstrap4',
    'widget_tweaks'
]

X_FRAME_OPTIONS='SAMEORIGIN' # only if django version >= 3.0

MIDDLEWARE = [
    # 'whitenoise.middleware.WhiteNoiseMiddleware',  # Static file handling
    'django.middleware.security.SecurityMiddleware',  # Security-related headers
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session management
    'django.middleware.common.CommonMiddleware',  # Common processing (e.g., URL handling)
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # User authentication
    'myproject.redirect_middleware.LoginRequiredMiddleware',  # Your custom middleware (Authentication-related?)
    'axes.middleware.AxesMiddleware',  # IP blocking for suspicious login attempts
    'myproject.middleware.AutoLogoutMiddleware',  # Automatic logout after inactivity
    'myproject.middleware.RedirectAfterInactivityMiddleware', #custom middleware
    'django.contrib.messages.middleware.MessageMiddleware',  # Message handling
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
    'myproject.middleware.UserSettingsMiddleware'
    
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'axes.backends.AxesStandaloneBackend',  # Use the new name
    # ...
]


# Configure the automatic logout time after inactivity (in seconds)
AUTO_LOGOUT_TIME = 600  # 10 minutes (adjust the value as needed)

# Configure Django Axes to track user activity for auto-logout
AXES_KEEP_RECORD = True
AXES_FAILURE_LIMIT = 5  # Number of allowed failures before blocking
AXES_COOLOFF_TIME = 1   # Time period (in hours) before login attempts reset
AXES_LOCK_OUT_AT_FAILURE = 10 #The number of failed login attempts after which a user's account is locked. 
AXES_MAX_FAILURES = 30 #Maximum number of failed login attempts allowed before locking out the user.
AXES_RESET_ON_SUCCESS = True #Reset
AXES_RESET_COOL_OFF_ON_FAILURE_DURING_LOCKOUT = False #

ROOT_URLCONF = 'myproject.urls'


LOGIN_EXEMPT_URLS = [
    r'^about/$',         # URL patterns that should be exempt from authentication
    r'^anouncement/$',
    r'^contacts/$',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'myapp.context_processors.include_login_form',
                'myapp.context_processors.user_profile',
                'myapp.context_processors.user_settings',

            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'bensonmwangi101@gmail.com'  # Use your Gmail email address
EMAIL_HOST_PASSWORD = 'Sulu5542'     # Use your Gmail password or app-specific password



# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if platform.system() == 'Windows':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',

        }
    }
elif platform.system() == 'Linux':
        DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'fertppm$fertdatabase',
            'USER': 'fertppm',
            'PASSWORD': 'Sulu5542',
            'HOST': 'fertppm.mysql.pythonanywhere-services.com',
            'PORT': '3306',

        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "productionfiles")
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'



STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'mystaticfiles'),  # Replace 'static' with your actual static files directory
]

WHITENOISE_MANIFEST_STRICT = False

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""

# Get the current host name
hostname = socket.gethostname()

# Define the base URL for your development server
DEV_SERVER_BASE_URL = 'http://127.0.0.1:8000'

# Define the base URL for your production server
PROD_SERVER_BASE_URL = 'https://www.pythonanywhere.com/'

# Determine the current server based on the hostname
if hostname == 'http://127.0.0.1:8000':
    BASE_URL = DEV_SERVER_BASE_URL
else:
    BASE_URL = PROD_SERVER_BASE_URL



# Set the session timeout to a longer duration (e.g., 30 minutes).
SESSION_COOKIE_AGE = 1800  # 30 minutes in seconds


# LOGIN_REDIRECT_URL = 'dasboard'
LOGOUT_REDIRECT_URL = 'index'  

LOGIN_URL = '/login/'  # Make sure this is set to your login URL
LOGIN_REDIRECT_URL = '/index/'  # Set this to your desired index URL


SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

ADMIN_LOGO = 'FERTPPM.jpeg'
MENU_WEIGHT = {
    'World': 20,
    'Auth': 4,
    'Sample': 5
}

ADMIN_STYLE = {
    'primary-color': 'blue',
    'secondary-color': 'pink',
    'tertiary-color': 'Yellow',
    'body-color': 'white',
    'backgound-color': 'black',
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
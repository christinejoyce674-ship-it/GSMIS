import os
from pathlib import Path

# 1. BASE DIRECTORY
# We use Path(__file__) to make path joining much easier and avoid TypeErrors
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. SECURITY SETTINGS
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'a&+18t7h@ll#4c8uvdh2oqv*p2_arcmo#e+=10bf*g0bgg4giw')
DEBUG = True
# WARNING: Remove '*' from ALLOWED_HOSTS before deploying to production!
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*', '[::1]']
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://localhost:8000']
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SAMESITE = 'Lax'
# 3. APP REGISTRATION
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app', 
    'active_link',
    
]

# 4. MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 4a. SESSION CONFIGURATION
# Allow multiple concurrent sessions for the same user
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 86400  # 24 hours in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
# This allows multiple logins from different browsers/devices
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

ROOT_URLCONF = 'GMIS.urls'

# 5. TEMPLATES
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
            ],
        },
    },
]

WSGI_APPLICATION = 'GMIS.wsgi.application'

# 6. DATABASE (FIXED)
# Removed the path to manage.py and fixed the slash operator error
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 7. PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = 'app:login'
# 8. STATIC & MEDIA FILES
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
SESSION_COOKIE_SECURE = False

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 9. CUSTOM USER MODEL
AUTH_USER_MODEL = 'app.CustomUser'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 10. AUTHENTICATION BACKENDS
# EmailBackEnd allows login with email instead of username
AUTHENTICATION_BACKENDS = [
    'app.EmailBackEnd.EmailBackEnd',
    'django.contrib.auth.backends.ModelBackend',  # fallback for Django admin
]

"""
Django settings for Hotel Management System.
Persian/Farsi Edition with RTL support.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-hotel-dev-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    # Django Unfold - MUST be before django.contrib.admin
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'unfold.contrib.inlines',
    
    # Django Core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third Party
    'corsheaders',
    'django_celery_results',
    
    # Local Apps
    'hotel',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
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
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database - PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'hotel_db'),
        'USER': os.environ.get('POSTGRES_USER', 'hotel'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'hotel_secure_password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =============================================================================
# LOCALIZATION - PERSIAN/FARSI SETTINGS
# =============================================================================
LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# RTL Languages
LANGUAGES = [
    ('fa', 'فارسی'),
    ('en', 'English'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# =============================================================================
# STATIC & MEDIA FILES
# =============================================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    BASE_DIR / 'staticfiles',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'hotel.User'

# =============================================================================
# CORS SETTINGS
# =============================================================================
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
CORS_ALLOW_CREDENTIALS = True

# =============================================================================
# CELERY CONFIGURATION
# =============================================================================
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Tehran'

# =============================================================================
# DJANGO UNFOLD CONFIGURATION - Professional Admin Panel
# =============================================================================
UNFOLD = {
    "SITE_TITLE": "سیستم مدیریت هتل",
    "SITE_HEADER": "سیستم مدیریت هتل",
    "SITE_SYMBOL": "hotel",
    "SITE_FAVICONS": [],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    
    # RTL Support
    "STYLES": [
        lambda request: "css/admin-rtl.css",
    ],
    
    # Sidebar Navigation
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "داشبورد",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "صفحه اصلی",
                        "icon": "home",
                        "link": "/admin/",
                    },
                ],
            },
            {
                "title": "مدیریت اتاق‌ها",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "اتاق‌ها",
                        "icon": "bed",
                        "link": "/admin/hotel/room/",
                    },
                    {
                        "title": "انواع اتاق",
                        "icon": "category",
                        "link": "/admin/hotel/roomtype/",
                    },
                ],
            },
            {
                "title": "رزرواسیون",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "رزروها",
                        "icon": "calendar_month",
                        "link": "/admin/hotel/booking/",
                    },
                    {
                        "title": "مهمانان",
                        "icon": "people",
                        "link": "/admin/hotel/guest/",
                    },
                ],
            },
            {
                "title": "مالی",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "پرداخت‌ها",
                        "icon": "payments",
                        "link": "/admin/hotel/payment/",
                    },
                ],
            },
            {
                "title": "کاربران",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "کاربران سیستم",
                        "icon": "person",
                        "link": "/admin/hotel/user/",
                    },
                ],
            },
        ],
    },
    
    # Dashboard Widgets (Callbacks)
    "DASHBOARD_CALLBACK": "hotel.admin.dashboard_callback",
    
    # Colors - Professional Hotel Theme
    "COLORS": {
        "primary": {
            "50": "#f0fdf4",
            "100": "#dcfce7",
            "200": "#bbf7d0",
            "300": "#86efac",
            "400": "#4ade80",
            "500": "#22c55e",
            "600": "#16a34a",
            "700": "#15803d",
            "800": "#166534",
            "900": "#14532d",
            "950": "#052e16",
        },
    },
}

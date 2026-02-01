import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'replace-this-with-secure-key-for-prod'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
    'products',
    'cart.apps.CartConfig',
    'orders',
    'search',
    'reviews',
    'django.contrib.sites',
    'django.contrib.humanize',
        # django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend', 
]
SITE_ID = 1

# Cấu hình đăng nhập bằng email
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # hoặc 'username_email' nếu muốn hỗ trợ cả username
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'  # hoặc 'optional'

# Redirect sau login/logout
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Social account provider settings for django-allauth
# Configure scopes and fields for OAuth providers (Google & Facebook)
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
        'SCOPE': ['email', 'public_profile'],
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'picture',
        ],
    },
}

ROOT_URLCONF = 'fashion_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.admin_statistics',
            ],
        },
    },
]

WSGI_APPLICATION = 'fashion_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Serve the project's `static/` directory inside the backend project
STATICFILES_DIRS = [ BASE_DIR / 'static' ]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MOMO_API_URL = "https://test-payment.momo.vn/v2/gateway/api/create"
MOMO_PARTNER_CODE = "MOMO"
MOMO_ACCESS_KEY = "F8BBA842ECF85"
MOMO_SECRET_KEY = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
CURRENT_SEASON = 'spring'


JAZZMIN_SETTINGS = {
    "site_title": "Fashion Admin",
    "site_header": "Fashion Store",
    "site_brand": "Quản lý Thời Trang",
    "welcome_sign": "Hệ thống quản lý bán hàng",
    "copyright": "Fashion Store Ltd",
    "search_model": ["orders.Order", "products.Product"],
    "topmenu_links": [
        {"name": "Trang chủ",  "url": "admin:index"},
        {"model": "orders.Order"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "orders.Order": "fas fa-cart-arrow-down",
        "products.Product": "fas fa-tshirt",
        "reviews.Review": "fas fa-comments",
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly", # Bạn có thể thử 'lux', 'darkly', 'cosmo'
    "navbar_small_text": False,
    "footer_small_text": False,
}


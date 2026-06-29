"""
Django settings for app project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security ─────────────────────────────────────────────────────────────────

SECRET_KEY = os.environ.get("SECRET_KEY", "changeme-replace-in-production")

DEBUG = bool(int(os.environ.get("DEBUG", 0)))

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
ALLOWED_HOSTS.extend(
    filter(None, os.environ.get("ALLOWED_HOSTS", "").split(","))
)

# ── Apps ──────────────────────────────────────────────────────────────────────

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "cloudinary_storage",
    "cloudinary",
    "core",
    "user",
    "recipe",
    "comments",
    "corsheaders",
]

# ── Middleware ────────────────────────────────────────────────────────────────

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

# ── Database ──────────────────────────────────────────────────────────────────
# Railway provides DATABASE_URL; fall back to individual vars for local Docker.

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    import urllib.parse
    url = urllib.parse.urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE":   "django.db.backends.postgresql",
            "NAME":     url.path.lstrip("/"),
            "USER":     url.username,
            "PASSWORD": url.password,
            "HOST":     url.hostname,
            "PORT":     url.port or 5432,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE":   "django.db.backends.postgresql",
            "HOST":     os.environ.get("DB_HOST"),
            "NAME":     os.environ.get("DB_NAME"),
            "USER":     os.environ.get("DB_USER"),
            "PASSWORD": os.environ.get("DB_PASS"),
        }
    }

# ── Password validation ───────────────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ── Internationalisation ──────────────────────────────────────────────────────

LANGUAGE_CODE = "en-us"
TIME_ZONE     = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ   = True

# ── Static files ──────────────────────────────────────────────────────────────

STATIC_URL  = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ── Media / uploaded images ───────────────────────────────────────────────────

CLOUDINARY_URL = os.environ.get("CLOUDINARY_URL")

if CLOUDINARY_URL:
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
    MEDIA_URL = "/media/"
else:
    MEDIA_URL  = "/static/media/"
    MEDIA_ROOT = "/vol/web/media"

# ── Auth & DRF ────────────────────────────────────────────────────────────────

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL    = "core.User"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "COMPONENT_SPLIT_REQUEST": True,
}

# ── CORS ──────────────────────────────────────────────────────────────────────

_cors_extra = os.environ.get("CORS_ALLOWED_ORIGINS", "")
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
] + [o for o in _cors_extra.split(",") if o]

CORS_ALLOW_CREDENTIALS = True

# Allow all Vercel preview deployment URLs automatically
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.vercel\.app$",
]

from .base import *
from decouple import config
import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DEBUG = False

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

CORS_ALLOW_ORIGIN_ALL = True
CORS_ALLOW_ALL_ORIGINS = True


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_USE_TLS = True


STATIC_URL = "/baa/static/"
STATIC_ROOT = "/home/gocrtjki/public_html/baa/static"
STATICFILES_DIRS = [BASE_DIR / "static", os.path.join(BASE_DIR, "front", "static")]

MEDIA_ROOT = "/home/gocrtjki/public_html/baa/media/"
# MEDIA_ROOT = '/home/gocrtjki/baa/baa'
MEDIA_URL = "/baa/media/"

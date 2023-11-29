import os

from .base import *

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

INSTALLED_APPS += [
    "django_extensions",
]


# REST_FRAMEWORK = {
#     # Use Django's standard `django.contrib.auth` permissions,
#     # or allow read-only access for unauthenticated users.
# }

# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, "tmp", "emails")


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# EMAIL_HOST = os.environ.get("EMAIL_HOST")
# EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
# EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = True


STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(REAL_BASE_DIR, "static")]
# STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

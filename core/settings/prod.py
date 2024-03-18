from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')

CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS").split(",")

CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

CSRF_USE_SESSIONS = True

CSRF_COOKIE_SAMESITE = 'None'

AWS_DEFAULT_ACL = 'public-read'
AWS_REGION = os.environ.get("AWS_REGION")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

if not all([AWS_REGION, AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY]):
    raise ValueError("AWS environment variables are not properly set.")

STORAGES = {
    "staticfiles": {
        "LOCATION": "static",
        "region_name": AWS_REGION,
        "DEFAULT_ACL": "public-read",
        "BUCKET_NAME": AWS_STORAGE_BUCKET_NAME,
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "default_acl": "public-read",
            "region_name": AWS_REGION,
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
        },
    },
}
import os
from pathlib import Path
from datetime import timedelta

# 배포 루틴
# poetry install > poetry export -f requirements.txt > requirements.txt
# > push > 도커에서 git pull > python manage.py crontab add > .env 변경해야하면 바꾸기.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")
CF_ID = os.environ.get("CF_ID")
CF_TOKEN = os.environ.get("CF_TOKEN")
GC_API_KEY = os.environ.get("GC_API_KEY")
GC_ID = os.environ.get("GC_ID")
GC_SECRET = os.environ.get("GC_SECRET")
NC_ID = os.environ.get("NC_ID")
NC_SECRET = os.environ.get("NC_SECRET")
KK_API_KEY = os.environ.get("KK_API_KEY")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = os.environ.get("EMAIL")
EMAIL_HOST_PASSWORD = os.environ.get("PASSWORD")
DEFAULT_FROM_MAIL = EMAIL_HOST_USER
FRONT_BASE_URL = "http://127.0.0.1:5500"
BACKEND_BASE_URL = "http://127.0.0.1:8000"
COUPANG_ACCESS_KEY = os.environ.get("COUPANG_ACCESS_KEY")
COUPANG_SECRET_KEY = os.environ.get("COUPANG_SECRET_KEY")
RF_API_KEY = os.environ.get("RF_API_KEY")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "taggit",
    "taggit_serializer",
    "users",
    "articles",
    "ai_process",
    "userlog",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_apscheduler",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "cookai.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "cookai.wsgi.application"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=240),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=2),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
}
# 환경변수에 따라 DEBUG모드 여부를 결정합니다.
DEBUG = os.environ.get("DEBUG", "0")

# DEBUG == "1" 이면 배포환경 "0" 이면 개발환경. 
if DEBUG == "1":
    DEBUG = False
    ALLOWED_HOSTS = [
        "localhost",
        "backend",
        "https://cookaiwork.com",
        "https://www.backend.cookai.today",
    ]
    LOG_DIR = os.path.join(BASE_DIR, "log")
    LOG_FILE = "/debug.log"
    LOG_PATH = LOG_DIR + LOG_FILE
    # LOGGING = {
    #     "version": 1,
    #     "disable_existing_loggers": False,
    #     "handlers": {
    #         "file": {
    #             "level": "ERROR",  # 로그 레벨
    #             "class": "logging.FileHandler",
    #             "filename": LOG_PATH,  # 로그 경로
    #         },
    #     },
    #     "loggers": {
    #         "django": {
    #             "handlers": ["file"],
    #             "level": "ERROR",
    #             "propagate": True,
    #         },
    #     },
    # }
    # LOGGING = {
    #     "version": 1,
    #     "disable_existing_loggers": False,
    #     "filters": {
    #         "require_debug_false": {
    #             "()": "django.utils.log.RequireDebugFalse",
    #         },
    #         "require_debug_true": {
    #             "()": "django.utils.log.RequireDebugTrue",
    #         },
    #     },
    #     "formatters": {
    #         "django.server": {
    #             "()": "django.utils.log.ServerFormatter",
    #             "format": "[{server_time}] {message}",
    #             "style": "{",
    #         },
    #         "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    #     },
    #     "handlers": {
    #         "console": {
    #             "level": "INFO",
    #             "filters": ["require_debug_true"],
    #             "class": "logging.StreamHandler",
    #         },
    #         "django.server": {
    #             "level": "INFO",
    #             "class": "logging.StreamHandler",
    #             "formatter": "django.server",
    #         },
    #         "mail_admins": {
    #             "level": "ERROR",
    #             "filters": ["require_debug_false"],
    #             "class": "django.utils.log.AdminEmailHandler",
    #         },
    #         "file": {
    #             "level": "INFO",
    #             "encoding": "utf-8",
    #             "filters": ["require_debug_false"],
    #             "class": "logging.handlers.RotatingFileHandler",
    #             "filename": LOG_PATH,
    #             "maxBytes": 1024 * 1024 * 5,  # 5 MB
    #             "backupCount": 5,
    #             "formatter": "standard",
    #         },
    #     },
    #     "loggers": {
    #         "django": {
    #             "handlers": ["console", "mail_admins", "file"],
    #             "level": "INFO",
    #         },
    #         "django.server": {
    #             "handlers": ["django.server"],
    #             "level": "INFO",
    #             "propagate": False,
    #         },
    #         "my": {
    #             "handlers": ["console", "file"],
    #             "level": "INFO",
    #         },
    #     },
    # }
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                "datefmt": "%d/%b/%Y %H:%M:%S",
            },
            "simple": {"format": "%(levelname)s %(message)s"},
        },
        "handlers": {
            "file": {
                "level": "ERROR",
                "encoding": "utf-8",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOG_PATH,
                "maxBytes": 1024 * 1024 * 5,  # 5 MB
                "backupCount": 5,
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["file"],
                "propagate": True,
                "level": "ERROR",
            },
        },
    }
    GC_API_KEY = os.environ.get("GC_DEPLOY_API_KEY")
    GC_ID = os.environ.get("GC_DEPLOY_ID")
    GC_SECRET = os.environ.get("GC_DEPLOY_SECRET")
    NC_ID = os.environ.get("NC_DEPLOY_ID")
    NC_SECRET = os.environ.get("NC_DEPLOY_SECRET")
    KK_API_KEY = os.environ.get("KK_DEPLOY_API_KEY")
    FRONT_BASE_URL = "https://cookai.today"
    BACKEND_BASE_URL = "https://www.backend.cookai.today"
    CORS_ALLOWED_ORIGINS = [
        "https://cookaiwork.com",
        "https://www.backend.cookai.today",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "https://cookaiwork.com",
        "https://www.backend.cookai.today",
    ]

elif DEBUG == "0":
    DEBUG = True
    ALLOWED_HOSTS = [
        "backend",
        "localhost",
        "127.0.0.1",
    ]
    GC_API_KEY = os.environ.get("GC_API_KEY")
    GC_ID = os.environ.get("GC_ID")
    GC_SECRET = os.environ.get("GC_SECRET")
    NC_ID = os.environ.get("NC_ID")
    NC_SECRET = os.environ.get("NC_SECRET")
    KK_API_KEY = os.environ.get("KK_API_KEY")
    FRONT_BASE_URL = "http://127.0.0.1:5500"
    BACKEND_BASE_URL = "http://127.0.0.1:8000"
    CORS_ALLOW_ALL_ORIGINS = True
    CSRF_TRUSTED_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# postgres 환경변수가 존재 할 경우에 postgres db에 연결을 시도합니다.
POSTGRES_DB = os.environ.get("POSTGRES_DB", "")
if POSTGRES_DB:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": POSTGRES_DB,
            "USER": os.environ.get("POSTGRES_USER", ""),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRES_HOST", ""),
            "PORT": os.environ.get("POSTGRES_PORT", ""),
        }
    }

# 환경변수가 존재하지 않을 경우 sqlite3을 사용합니다.
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_USER_MODEL = "users.User"
# Format string for displaying run time timestamps in the Django admin site. The default
# just adds seconds to the standard Django format, which is useful for displaying the timestamps
# for jobs that are scheduled to run on intervals of less than one minute.
# See https://docs.djangoproject.com/en/dev/ref/settings/#datetime-format for format string
# syntax details.
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
# Maximum run time allowed for jobs that are triggered manually via the Django admin site, which
# prevents admin site HTTP requests from timing out.
# Longer running jobs should probably be handed over to a background task processing library
# that supports multiple background worker processes instead (e.g. Dramatiq, Celery, Django-RQ,
# etc. See: https://djangopackages.org/grids/g/workers-queues-tasks/ for popular options).
APSCHEDULER_RUN_NOW_TIMEOUT = 100  # Seconds
SCHEDULER_DEFAULT = True  # apps.py 참고

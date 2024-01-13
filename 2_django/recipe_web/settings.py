import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')


SECRET_KEY = 'bzyjrsylze82ev_j2y4o3zju$sjkug^_w&f(88ii4=178z9t7m'

import json_log_formatter

class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        self.datefmt = "%Y-%m-%d %H:%M:%S"
        extra['asctime'] = self.formatTime(record, self.datefmt)
        return extra

    
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
        "formatters": {
        "json":{
            "()": CustomisedJSONFormatter,
        }
    },
    "handlers": {
        "file2": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, 'logsfolder') + "/json_log.log",
            "formatter": "json",
        },
    },
    "loggers": {
        'file2': {
            'handlers': ['file2'],
            'level': 'INFO',
            'propagate': False,
        }

    },
}


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'posts',
    'accounts',
    
    'bootstrap5',
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

ROOT_URLCONF = 'recipe_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ MAIN_TEMPLATE_DIR ],
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

WSGI_APPLICATION = 'recipe_web.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': '보안상 삭제', # 사용할 데이터베이스 엔진
        'NAME': '보안상 삭제', # 데이터베이스 이름 
        'USER': '보안상 삭제', # 접속할 Database 계정 아이디 ex) root
        'PASSWORD': '보안상 삭제',  # 접속할 Database 계정 비밀번호 ex) 1234
        'HOST': '보안상 삭제',   # host는 로컬 환경에서 동작한다면 ex) localhost
        'PORT': '보안상 삭제', # 설치시 설정한 port 번호를 입력한다. ex) 3306
        'OPTIONS': {
    'auth_plugin': 'mysql_native_password',  # 'caching_sha2_password' 대신 'mysql_native_password' 사용
}
    }
}

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'

AUTH_USER_MODEL = 'accounts.User'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/' 
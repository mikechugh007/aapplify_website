from email.policy import default
from pathlib import Path
from datetime import timedelta
from django.conf import settings
from decouple import config
import os


BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = config("DJ_SECRET_KEY")
TEMPLATE_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'


DEBUG = True
SESSION_COOKIE_SECURE = False  # Set to False if testing on local development server
CSRF_COOKIE_SECURE = False    # Set to False if testing on local development server


ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
		'jazzmin',
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.messages',
		'django.contrib.staticfiles',
		"django_browser_reload",
		"django_ckeditor_5",
		"sorl.thumbnail",
		"rest_framework",
		"rest_framework_simplejwt",
		'mainapp',
		'corsheaders',
		'authentication',
		'service_email',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.common.CommonMiddleware',
    'aapplify.middlewares.DisableCSRFMiddleware',
	# 'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	# "django_browser_reload.middleware.BrowserReloadMiddleware",
  

]

CORS_ALLOW_ALL_ORIGINS = True  # If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect

ROOT_URLCONF = 'aapplify.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'aapplify.wsgi.application'
AUTH_USER_MODEL="authentication.User"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'db.sqlite3',
	}
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	# {
	# 	'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	# },
	# {
	# 	'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	# },
	# {
	# 	'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	# },
	# {
	# 	'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	# },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [STATIC_DIR]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mail.aapplify.com"  # HostGator mail server
EMAIL_PORT = 465  # SSL port (or 587 for TLS)
EMAIL_USE_SSL = True  # Use SSL (set to False and use EMAIL_USE_TLS=True for port 587)
EMAIL_USE_TLS = False
EMAIL_HOST_USER = config("SMTP_EMAIL", default="support@aapplify.com")  # Your full email address
EMAIL_HOST_PASSWORD = config("SMTP_APP_PASSWORD", default="your-email-password")  # Your email password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

STRIPE_PUBLIC_KEY=config("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY=config("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET=config("STRIPE_WEBHOOK_SECRET")

BASE_URL = config("BASE_URL",default="http://localhost:8000")


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES': (
		'rest_framework.permissions.IsAuthenticated',
	),
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework_simplejwt.authentication.JWTAuthentication',
	),
}

SIMPLE_JWT = {
  'ACCESS_TOKEN_LIFETIME': timedelta(minutes=180),
	'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
}



customColorPalette = [
		{
			'color': 'hsl(4, 90%, 58%)',
			'label': 'Red'
		},
		{
			'color': 'hsl(340, 82%, 52%)',
			'label': 'Pink'
		},
		{
			'color': 'hsl(291, 64%, 42%)',
			'label': 'Purple'
		},
		{
			'color': 'hsl(262, 52%, 47%)',
			'label': 'Deep Purple'
		},
		{
			'color': 'hsl(231, 48%, 48%)',
			'label': 'Indigo'
		},
		{
			'color': 'hsl(207, 90%, 54%)',
			'label': 'Blue'
		},
	]

CKEDITOR_5_CONFIGS = {
	'default': {
		'toolbar': ['heading', '|', 'bold', 'italic', 'link',
					'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],

	},
	'extends': {
		'blockToolbar': [
			'paragraph', 'heading1', 'heading2', 'heading3',
			'|',
			'bulletedList', 'numberedList',
			'|',
			'blockQuote',
		],
		'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
		'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
					'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
					'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
					'insertTable',],
		'image': {
			'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
						'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
			'styles': [
				'full',
				'side',
				'alignLeft',
				'alignRight',
				'alignCenter',
			]

		},
		'table': {
			'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
			'tableProperties', 'tableCellProperties' ],
			'tableProperties': {
				'borderColors': customColorPalette,
				'backgroundColors': customColorPalette
			},
			'tableCellProperties': {
				'borderColors': customColorPalette,
				'backgroundColors': customColorPalette
			}
		},
		'heading' : {
			'options': [
				{ 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
				{ 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
				{ 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
				{ 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
			]
		}
	},
	'list': {
		'properties': {
			'styles': 'true',
			'startIndex': 'true',
			'reversed': 'true',
		}
	}
}

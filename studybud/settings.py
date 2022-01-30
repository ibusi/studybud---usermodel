"""
Django settings for studybud project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fm3wsoh_lec%bt%u^q&tv*88_c9_ody(8bp9p^xc1bo6*syq(#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


#INSTALLED_APPSは環境変数。
#これはDjangoインスタンスの中で有効化されているすべてのDjangoアプリケーションの名前を保持するリストの環境変数。
#django-admin startproject で作成されたDjangoアプリケーションの INSTALLED_APPS はデフォルトで
#django.contrib~等いくつかアプリケーションを保持しています。

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',

    #Cookie（クッキー）とは、Webサーバーがクライアントコンピュータに預けておく小さなファイルのこと。
    #クライアントコンピュータが、あるWebサーバーに初めて接続した際に、Webサーバーがクライアントコンピュータの中に、
    #そのWebサーバー専用のCookieファイルを作成する。
    #そして、次回、クライアントコンピュータがWebサーバーに接続したときには、WebブラウザがそのCookieをWebサーバーに
    #送信する。このような仕組みによって、Webサーバーは、個々のクライアントコンピュータが前回使用していた情報を読み取ること
    #ができるようになる。Cookieには、Webサーバーによってどのような情報でも格納できるが、多くの場合は、
    #ユーザー名などの接続情報、ショッピングサイトなどで購入する商品を一時的に保管する
    # “買い物かご”の情報、氏名や住所、電話番号などの一度登録した会員情報といった管理に利用される。

    #sessionとは、通信の始まりから終わりまでを一つの単位としたまとまり。
    #Djangoではsessionフレームワークを使うことで、データをサイト訪問者単位で扱うことが出来るようになる。
    #sessionでは主にログインページなどでログインしているかどうかなどを管理する。
    #あくまでも、一つの通信に対して使われるのではなくてログインからログアウトまでを1つのsessionとして扱う。
    #Djangoのデフォルト設定では、セッションはwebサーバーに保存されるようになっている。
    #セッションはデータベースに保存するがユーザーを識別するsessionidというものがありログインした際に作成され
    #Cookieはsessionidを記録する
    #sessionはWEBページを閉じるまで保存をするのでその都度sessionidは違う

    #adminページからユーザーがログインする際にcsrfトークンが作られる
    #chromeのf12→application→Cookiesでログインした時のトークンの発行やsessionidが確認できる
    #ログイン後も他のアドミンのページ内を移動するときは都度チェックする
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #python manage.py startapp baseでbaseフォルダーを作ったのでその中の
    #base/apps.pyのclass BaseConfigとを紐づけbaseフォルダーおよび以下のアプリやモデルを有効かする
    'base.apps.BaseConfig',

    #restframeworkをインストールした後はここに記述する必要がある
    'rest_framework',

    'corsheaders',
]

# Djangoには標準で備わっている強力なUserモデルが存在し、viewなどからはdjango.contrib.auth.modelsのUserを参照することで
# 利用することができる。しかし、※Djangoの公式ドキュメントでも言及されている通り、自分のプロジェクトのなかでこのデフォルト
# のUserモデルをそのまま利用するのは避けるべき。その場合、独自に定義したカスタムユーザーを作成することになるが、
# その場合のUserモデルへの参照方法の一つがAUTH_USER_MODELを参照すること

AUTH_USER_MODEL = 'base.User'

# Djangoの文脈でMiddlewareとは
# リクエストが送られた時に行う処理
# レスポンスを返す前に行う処理
# などを定義することができるもの
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    "corsheaders.middleware.CorsMiddleware",

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#一番最初に参照するURLのフォルダーを指定する
ROOT_URLCONF = 'studybud.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS'　デフォルト値: [] (空のリスト)
        #Directories where the engine should look for template source files, in search order.
        #プロジェクトのベースフォルダを示します。
        'DIRS': [
            BASE_DIR / 'templates'
        ],
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

WSGI_APPLICATION = 'studybud.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# URL that handles the media served from MEDIA_ROOT
MEDIA_URL = '/images/'

#これによりstaticファイルが存在することを知らせる事ができる
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# フォームでデータが登録された時に、ピクチャがどこにアップロードされるかを指定する
MEDIA_ROOT = BASE_DIR / 'static/images'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

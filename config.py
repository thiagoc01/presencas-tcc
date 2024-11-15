import dotenv

env = dotenv.dotenv_values('.env')

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = env.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = env.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 16
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    TOKEN_REQUISICOES = env.get("TOKEN_REQUISICOES")
    CKAN_URL = env.get("CKAN_URL")
    REMEMBER_COOKIE_NAME="presencas_sessao"
    SESSION_PERMANENT = bool(env.get("SESSION_PERMANENT", False))
    PERMANENT_SESSION_LIFETIME = int(env.get("PERMANENT_SESSION_LIFETIME", 3600))


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///testdb.sqlite"
    REMEMBER_COOKIE_DURATION=86400
    SESSION_PERMANENT = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///testdb.sqlite"
    BCRYPT_LOG_ROUNDS = 1
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    DEBUG_TB_ENABLED = False
    REMEMBER_COOKIE_DURATION=2592000

import dotenv

env = dotenv.dotenv_values('.env')

DATABASE_URI = env.get("DATABASE_URL")
if DATABASE_URI.startswith("postgres://"):
    DATABASE_URI = DATABASE_URI.replace("postgres://", "postgresql://", 1)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = env.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    TOKEN_REQUISICOES = env.get("TOKEN_REQUISICOES")
    CKAN_URL = env.get("CKAN_URL")
    REMEMBER_COOKIE_NAME="presencas_sessao"



class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///testdb.sqlite"
    REMEMBER_COOKIE_DURATION=86400


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

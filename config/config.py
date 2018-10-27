import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Common configurations"""
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY: secrets.token_hex(16)
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")


class DevelopmentConfig(Config):
    """Development configurations"""
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """Testing configurations"""
    TESTING = True


class ProductionConfig(Config):
    """Production configurations"""
    DEBUG = False


app_settings = {
    "development": "config.config.DevelopmentConfig",
    "testing": "config.config.TestingConfig",
    "production": "config.config.ProductionConfig"
}

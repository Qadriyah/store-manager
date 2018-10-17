import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Common configurations"""
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY: "mukunguB"


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
    "development": "config.DevelopmentConfig",
    "testing": "config.TestingConfig",
    "production": "config.ProductionConfig"
}

import os


class Config:
    """ Base configuration class """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = os.getenv('JWT_BLACKLIST_ENABLED')
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    APP_SETTINGS = os.getenv('development')
    

class DevelopmentConfig(Config):
    """Configurations for Development"""
    DEBUG = True
    TESTING = False
    DATABASE_URI = os.getenv('DATABASE_URL')


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database"""
    TESTING = True
    DEBUG = True
    DATABASE_URI = os.getenv('TEST_DATABASE_URL')


class StagingConfig(Config):
    """Configurations for Staging"""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Productions"""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}

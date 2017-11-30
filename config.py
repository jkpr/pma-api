"""Application configuration classes."""
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration."""
    TESTING = False
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    """Test configuration."""
    db_url = 'postgresql+psycopg2://pmaapi:pmaapi@localhost/pmaapi'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', db_url) + '-test'
    SQLALCHEMY_ECHO = False
    TESTING = True
    SERVER_NAME = 'localhost:5000'


class StagingConfig(Config):
    """Staging configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class ProductionConfig(Config):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLITE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.db')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', SQLITE_URI)


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'staging': StagingConfig,
    'test': TestConfig,
    # And the default is...
    'default': DevelopmentConfig
}

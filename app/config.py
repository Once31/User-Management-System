import os, datetime

_deployed_env_ = os.environ.get('FLASK_ENV', default=None)

print(f'environment: [{_deployed_env_}]')

class Config(object):
    TESTING = False
    DEBUG = False
    JWT_SECRET_KEY = 'THIS_IS_SECRET_KEY'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=1)
    UMS_ADMIN_EMAIL = 'ajay@gmail.com'
    UMS_ADMIN_PASSWORD =  'ajay123'


class ProductionConfig(Config):
    DATABASE_URI = 'user-management-prod.db'

class DevelopmemntConfig(Config):
    DATABASE_URI = 'user-management-dev.db'
    TESTING = True
    DEBUG = True

class TestingConfig(Config):
    DATABASE_URI = 'user-management-test.db'
    TESTING = True

def load_configuration(app):
    # print(_deployed_env_)
    if(_deployed_env_ == None):
        app.config.from_object(DevelopmemntConfig)
    elif(_deployed_env_ == 'dev'):
        app.config.from_object(DevelopmemntConfig)
    elif(_deployed_env_ == 'testing'):
        app.config.from_object(TestingConfig)
    elif (_deployed_env_ == 'production'):
        app.config.from_object(ProductionConfig)
    else:
        raise RuntimeError('Unknown environment settings provided.')

import os


class BaseConfig:
    '''配置基类
    '''

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'haha'


class DevConfig(BaseConfig):
    '''开发环境配置类
    '''

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost:3306/qa?charset=utf8'


class ProConfig(BaseConfig):
    pass


configs = {'dev': DevConfig, 'pro': ProConfig}

# -*- coding:utf-8 -*-
import logging
from datetime import timedelta


class Config(object):
    """工程配置信息"""

    DEBUG = True

    # 配置redis配置信息
    REDIS_HOST = "172.19.193.244"
    REDIS_PORT = 6300

    # 配置数据库
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = 'root'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'Mocha_ITOM'

    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECRET_KEY = "asldjasldkjal*(**d9dsefs"
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)  # 配置1天有效

    # # 将session调整到redis数据库保存的配置信息
    # SESSION_TYPE = "redis"
    # # 具体保存到那个数据库，redis数据库对象
    # # session["key"] = value  ---> 数据保存到1号数据库   session: key valye
    # SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=1)
    # # 对session_id需要加密处理
    # SESSION_USE_SIGNER = True
    # # 不需要永久存储
    # SESSION_PERMANENT = Falses
    # # 设置有效存储时间为(单位s)：24小时
    # PERMANENT_SESSION_LIFETIME = 86400


class DevelopmentConfig(Config):
    """开发模式"""

    DEBUG = True

    # 设置日志级别为：DEBUG
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    """生产模式"""

    DEBUG = False
    # 配置数据库
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'koms'
    PASSWORD = 'koms123456'
    HOST = '192.168.106.162'
    PORT = '3306'
    DATABASE = 'koms'

    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 设置日志级别为：INFO
    LOG_LEVEL = logging.INFO


class_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

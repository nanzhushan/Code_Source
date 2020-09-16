#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2020/4/22 11:37 
# @Author : zqy
import datetime
import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, request, abort, current_app, render_template, g
from flask_sqlalchemy import SQLAlchemy

from config import class_dict
from oms.constants import IP_WHITE_LIST

from flask_cors import CORS

db = SQLAlchemy()


def write_log(config_class):
    """不同的app模式对应不同的日志类型"""

    if not os.path.exists("logs"):
        os.makedirs("logs")

    if config_class.DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # 所有日志格式：
    rf_handler = logging.handlers.TimedRotatingFileHandler('logs/all.log', when='midnight', interval=1,
                                                           backupCount=7, atTime=datetime.time(0, 0, 0, 0))
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # 错误日志格式：
    f_handler = logging.FileHandler('logs/error.log')
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

    # 给logger添加handler
    logging.getLogger().addHandler(rf_handler)
    logging.getLogger().addHandler(f_handler)


def create_app(class_modul):
    app = Flask(__name__, static_url_path="/static")

    # 根据传入的不同配置模式，获取不同的配置信息
    config_class = class_dict[class_modul]

    # 加载配置文件
    app.config.from_object(config_class)

    if not os.path.exists("data"):
        os.makedirs("data")

    # 记录日志
    write_log(config_class)

    CORS(app, supports_credentials=True)

    # 连接mysql数据库
    try:
        db.init_app(app)
    except Exception:
        raise TimeoutError(u"连接mysql数据库失败！！请检查是否开启与配置正确。")

    # TODO 注册蓝图对象
    from oms.apps.user import index_bp
    app.register_blueprint(index_bp)

    from oms.apps.assetManage import index_bp
    app.register_blueprint(index_bp)

    from oms.apps.deployManage import index_bp
    app.register_blueprint(index_bp)

    from oms.apps.faultManage import index_bp
    app.register_blueprint(index_bp)

    from oms.apps.monitorManage import index_bp
    app.register_blueprint(index_bp)

    from oms.apps.installList import index_bp
    app.register_blueprint(index_bp)

    @app.route("/favicon.ico")
    def get_favicon():
        return current_app.send_static_file("img/favicon.ico")

    from oms.utils.common import get_user_info
    @app.route("/")
    @get_user_info
    def index():
        return render_template("index.html", username=g.user.username)

    @app.route("/init_mysql")
    def init_mysql():
        db.create_all()
        return "ok"

    return app

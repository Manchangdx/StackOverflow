from flask import Flask, render_template

from .handlers import blueprint_list
from .configs import configs
from .models import db, User


def create_app(config):
    app = Flask(__name__)
    # app.config 是一个类字典对象，它有一个 from_object 方法
    # 此方法可以将类的实例作为参数，从中读取配置项
    # 注意读取的配置项为全大写的类属性
    # 所以 configs.py 文件中的类属性名应为全大写，用下划线连接
    app.config.from_object(configs.get(config))
    db.init_app(app)
    for bp in blueprint_list:
        app.register_blueprint(bp)
    return app

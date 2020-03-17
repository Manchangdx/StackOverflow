from flask import Flask, render_template
from flask_login import LoginManager

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

    login_manager = LoginManager()
    login_manager.init_app(app)
    # 如果未登录用户发起了需要登录才能正确响应的请求
    # 调用 front 蓝图的 login 函数处理
    login_manager.login_view = 'front.index'
    # 当用户登录时，服务器会创建会话并将其标记为“活跃”状态
    # 当会话被销毁，用户通过 Cookies 重新登录，新建会话被标记为“非活跃”状态
    # 如果登录用户处于非活跃状态，对于一些敏感操作的请求，例如修改密码
    # 调用 front 蓝图的 login 函数处理
    login_manager.refresh_view = 'front.index'

    # 该方法利用会话中存储的 id 字段查询并加载用户，使之处于登录状态
    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    return app

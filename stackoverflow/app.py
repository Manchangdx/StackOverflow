from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from .models import db, User
from .config import configs
from .handlers import blueprint_list


def register_extensions(app):
    for blueprint in blueprint_list:
        app.register_blueprint(blueprint)
    db.init_app(app)
    Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    # 如果未登录用户发起了需要登录才能正确响应的请求
    # 调用 front 蓝图的 login 函数处理
    login_manager.login_view = 'front.login'
    # 当用户登录时，服务器会创建会话并将其标记为“活跃”状态
    # 当会话被销毁，用户通过 Cookies 重新登录，新建会话被标记为“非活跃”状态
    # 如果登录用户处于非活跃状态，对于一些敏感操作的请求，例如修改密码
    # 调用 front 蓝图的 login 函数处理
    login_manager.refresh_view = 'front.login'

    # 该方法利用会话中存储的 id 字段查询并加载用户，使之处于登录状态
    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_extensions(app)

    return app

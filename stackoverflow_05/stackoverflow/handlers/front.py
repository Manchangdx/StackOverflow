from flask import Blueprint, render_template
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required

from ..models import db, User


front = Blueprint('front', __name__)


# 首页
@front.route('/')
def index():
    return render_template('index.html', title='Stack Overflow 首页',
            tem_str='shiyanlou')


# 注册
@front.route('/signup', methods=['POST'])
def signup():
    # 根据表单信息查询 user 数据表
    # 如果 name 或 email 字段已经存在，返回 JSON 响应
    user = User.query.filter(
        (User.name==request.form['name']) | (User.email==request.form['email'])
    ).first()
    if user:
        return jsonify(status="error", info="已存在该用户")
    # 创建用户实例，在创建过程中会自动对 password 属性进行哈希运算
    user = User(name=request.form['name'], email=request.form['email'],
            password=request.form['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(status="success", info="创建成功")


# 登录
@front.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(name=request.form['name']).first()
    if user:
        if user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('.index'))
        return jsonify(status="error", info="密码错误")
    return jsonify(status="error", info="用户不存在")


# 退出登录
@front.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))

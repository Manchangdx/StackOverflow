from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    '''用户数据表映射类
    '''

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    _password = db.Column('password', db.String(256), nullable=False)

    @property
    def password(self):
        return self._password

    # 创建用户实例时会自动调用此方法对 password 属性进行哈希运算
    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    def __repr__(self):
        return '<User: {}>'.format(self.name)

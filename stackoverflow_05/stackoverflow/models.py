from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()


class User(db.Model, UserMixin):
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


class Question(db.Model):
    '''问题数据表映射类
    '''

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text(2048))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id',
            ondelete='CASCADE'))
    author = db.relationship('User', backref=db.backref('questions',
            lazy='dynamic'))
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<User: {}>'.format(self.title)


class Answer(db.Model):
    '''回答数据表映射类
    '''

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(2048))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id',
            ondelete='CASCADE'))
    author = db.relationship('User', backref=db.backref('answers',
            lazy='dynamic'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id',
            ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answers',
            lazy='dynamic'))
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Answer: {} - {}>'.format(self.question.title, self.author.name)


class Comment(db.Model):
    '''评论数据表映射类
    '''

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(2048))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id',
            ondelete='CASCADE'))
    author = db.relationship('User', backref=db.backref('comments',
            lazy='dynamic'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id',
            ondelete='CASCADE'))
    answer = db.relationship('Answer', backref=db.backref('comments',
            lazy='dynamic'))
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Comment: {} - {}>'.format(self.answer.id, self.author.name)

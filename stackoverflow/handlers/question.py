from flask import (Blueprint, render_template, request, jsonify, redirect,
        url_for, current_app)
from flask_login import login_required, current_user

from ..models import db, User, Question, Answer, Comment


question = Blueprint('question', __name__, url_prefix='/question')


# 问题列表页
@question.route('/')
def question_list():
    questions = Question.query.all()
    return render_template('question/list.html', questions=questions)


# 增加问题的页面
@question.route('/add', methods=['GET', 'POST'])
@login_required
def add_question():
    if request.method == 'POST':
        if Question.query.filter_by(title=request.form['title']).first():
            return jsonify(status="error", info="该问题已存在")
        question = Question(author=current_user, title=request.form['title'],
                content=request.form['content'])
        db.session.add(question)
        db.session.commit()
        return jsonify(status="success", info="问题创建成功")
    return render_template('question/ask.html')


# 问题详情页
@question.route('/<int:id>')
def question_detail(id):
    question = Question.query.get(id)
    if question:
        return render_template('question/detail.html', question=question)
    current_app.logger.error('问题不存在')
    # 如果问题不存在，跳转到问题列表
    return redirect(url_for('.question_list'))


# 添加答案或答案的评论
@question.route('/<int:id>/add_answer', methods=['POST'])
@login_required
def add_answer(id):
    # 如果 rtype 为 1 则表示添加答案，如果 rtype 为 2 则表示添加答案的评论
    if request.form['rtype'] == '1':
        question = Question.query.get(id)
        if not question:
            return jsonify(status="error", info="该问题不存在")
        answer = Answer(content=request.form['content'], author=current_user,
                question=question)
        db.session.add(answer)
        db.session.commit()
        return jsonify(status="success", info="答案提交成功")
    if request.form['rtype'] == '2':
        answer = Answer.query.get(id)
        comment = Comment(content=request.form['content'], author=current_user,
                answer=answer)
        db.session.add(comment)
        db.session.commit()
        return jsonify(status="success", info="对答案的评论提交成功")

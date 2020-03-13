from flask import blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user

from ..models import db, User, Question, Answer, Comment


answer = Blueprint('answer', __name__, url_prefix='/answer')


@answer.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def add_answer

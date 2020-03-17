from flask import Blueprint, render_template


front = Blueprint('front', __name__)


@front.route('/')
def index():
    return render_template('index.html', title='Stack Overflow 首页',
            tem_str='shiyanlou')

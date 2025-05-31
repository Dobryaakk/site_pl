from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/vacancies')
def vacancies():
    return render_template('vacancies.html')

@bp.route('/legalization')
def legalization():
    return render_template('legalization.html') 
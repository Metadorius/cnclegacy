from flask import render_template, flash, redirect, url_for
from webapp import app
from webapp.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from webapp.models import *
from unidecode import unidecode


@app.template_filter('cc')
def camel_casify(column):
    first, *rest = column.split(' ')
    return first.lower() + ''.join(word.lower().capitalize() for word in rest)


@app.template_filter('tr')
def transliterate(s):
    return unidecode(s)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_login=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Неверные логин или пароль!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Войти', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', menu_items=MenuItem.query.filter_by(parent_id=None).all())

from flask import render_template, flash, redirect, url_for, request
from webapp import app
from webapp.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from webapp.models import *
from unidecode import unidecode
from werkzeug.urls import url_parse
from datetime import datetime


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
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Войти', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def root():
    return redirect(url_for('index'))


@app.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    pages = Page.query.filter_by(page_visible=True).filter(Page.page_timestamp <= datetime.utcnow()).order_by(Page.page_timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    menu_items = MenuItem.query.filter_by(parent_id=None).all()
    
    return render_template('index.html',
        menu_items=menu_items,
        pages=pages)


@app.route('/page/<url>')
def full_page(url):
    page = Page.query.filter_by(page_url=url, page_visible=True).filter(Page.page_timestamp <= datetime.utcnow()).first_or_404()
    menu_items = MenuItem.query.filter_by(parent_id=None).all()

    return render_template('page.html', menu_items=menu_items, page=page)


@app.route('/user/<username>', methods=['GET', 'POST'])
def user_page(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(user_login=username).first_or_404()
    user_pages = user.user_pages.filter_by(page_visible=True).filter(Page.page_timestamp <= datetime.utcnow()).order_by(Page.page_timestamp.desc())
    menu_items = MenuItem.query.filter_by(parent_id=None).all()
    return render_template('user.html',
        menu_items=menu_items,
        datetime=datetime,
        user=user,
        user_pages=user_pages,
        page_num=page,
        per_page=app.config['POSTS_PER_PAGE'])


@app.route('/tags')
def tags_page():
    tags = Tag.query.all()
    tags.sort(key=lambda i: len(i.tag_pages.all()), reverse=True)
    menu_items = MenuItem.query.filter_by(parent_id=None).all()

    return render_template('tags.html',
        menu_items=menu_items,
        tags=tags)

@app.route('/tags/<tag_name>', methods=['GET', 'POST'])
def tag_page(tag_name):
    page = request.args.get('page', 1, type=int)
    tag = Tag.query.filter_by(tag_name=tag_name).first_or_404()
    tag_pages = Page.query.filter(Page.page_tags.any(tag_name=tag_name)).filter_by(page_visible=True).filter(Page.page_timestamp <= datetime.utcnow()).order_by(Page.page_timestamp.desc())
    menu_items = MenuItem.query.filter_by(parent_id=None).all()

    return render_template('tag_pages.html',
        menu_items=menu_items,
        tag=tag,
        tag_pages=tag_pages,
        page_num=page,
        per_page=app.config['POSTS_PER_PAGE']
    )


from datetime import datetime
from webapp import db, login
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin

# User things


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


role_perm = db.Table(
    'role_perm',
    db.Column('role_id', db.Integer, db.ForeignKey('role.role_id')),
    db.Column('perm_id', db.Integer, db.ForeignKey('perm.perm_id')),
    db.PrimaryKeyConstraint('role_id', 'perm_id')
)


class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key =True)
    role_name = db.Column(db.String(32), index=True,
                          unique=True, nullable=False)

    role_users = db.relationship('User', backref='user_role', lazy='dynamic')
    role_perms = db.relationship(
        'Perm', lazy='dynamic', secondary=role_perm, backref='perm_roles')

    def __repr__(self):
        return '<Role {}>'.format(self.role_name)


class Perm(db.Model):
    perm_id = db.Column(db.Integer, primary_key=True)
    perm_name = db.Column(db.String(32), index=True,
                          unique=True, nullable=False)

    def __repr__(self):
        return '<Perm {}>'.format(self.perm_name)


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(32), index=True,
                           unique=True, nullable=False)
    user_password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)

    user_pages = db.relationship('Page', backref='page_author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.user_name)

    @property
    def user_password(self):
        raise AttributeError('password is not a readable property')

    @user_password.setter
    def user_password(self, user_password):
        self.user_password_hash = generate_password_hash(user_password)

    def verify_password(self, password):
        return check_password_hash(self.user_password_hash, password)


# Menu


menu_page = db.Table(
    'menu_page',
    db.Column('item_id', db.Integer, db.ForeignKey('menu_item.item_id')),
    db.Column('page_id', db.Integer, db.ForeignKey('page.page_id'), nullable=False),
    db.PrimaryKeyConstraint('item_id')
)


class MenuItem(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(32), index=True,
                          unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey(
        'menu_item.item_id'), nullable=True)

    item_subitems = db.relationship(
        'MenuItem', backref='item_parent', lazy='dynamic')

    item_link = db.relationship(
        'MenuLink', backref='menu_item', lazy='dynamic', uselist=False)
    item_page = db.relationship(
        'Page', lazy='dynamic', secondary=menu_page, backref='menu_item', uselist=False)

    def __repr__(self):
        return '<MenuItem {}>'.format(self.item_name)


class MenuLink(db.Model):
    item_id = db.Column(db.Integer, db.ForeignKey(
        'menu_item.item_id'), primary_key=True)
    item_link = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<MenuLink {}>'.format(self.item_link)

# Tags


page_tag = db.Table(
    'page_tag',
    db.Column('page_id', db.Integer, db.ForeignKey('page.page_id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id')),
    db.PrimaryKeyConstraint('page_id', 'tag_id')
)


class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(32), index=True,
                         unique=True, nullable=False)

    def __repr__(self):
        return '<Tag {}>'.format(self.tag_name)


# Files

page_file = db.Table(
    'page_file',
    db.Column('page_id', db.Integer, db.ForeignKey('page.page_id')),
    db.Column('file_id', db.Integer, db.ForeignKey('file.file_id')),
    db.PrimaryKeyConstraint('page_id', 'file_id')
)


class File(db.Model):
    file_id = db.Column(db.Integer, primary_key=True)
    file_loc = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<File {}>'.format(self.file_name)


# pages

class Page(db.Model):
    page_id = db.Column(db.Integer, primary_key=True)
    page_title = db.Column(db.String(64), index=True,
                           unique=True, nullable=False)
    page_url = db.Column(db.String(64), unique=True, nullable=False)
    page_timestamp = db.Column(
        db.DateTime, index=True, default=datetime.utcnow)
    page_visible = db.Column(db.Boolean, index=True,
                             default=True, nullable=False)
    page_preview = db.Column(db.Text)
    page_content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    page_tags = db.relationship(
        'Tag', lazy='dynamic', secondary=page_tag, backref='tag_pages')
    page_files = db.relationship(
        'File', lazy='dynamic', secondary=page_file, backref='file_pages')

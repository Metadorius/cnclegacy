from datetime import datetime
from webapp import db, login
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

# User things


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


role_perm = db.Table(
    'role_perm',
    db.Column('role_id', db.Integer, db.ForeignKey(
        'role.role_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('perm_id', db.Integer, db.ForeignKey(
        'perm.perm_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.PrimaryKeyConstraint('role_id', 'perm_id')
)


class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(32), index=True,
                          unique=True, nullable=False)

    role_users = db.relationship('User', backref='user_role', lazy='dynamic')
    role_perms = db.relationship(
        'Perm', lazy='dynamic', secondary=role_perm, backref='perm_roles')

    def __repr__(self):
        return self.role_name


class Perm(db.Model):
    perm_id = db.Column(db.Integer, primary_key=True)
    perm_name = db.Column(db.String(32), index=True,
                          unique=True, nullable=False)

    def __repr__(self):
        return self.perm_name


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(32), index=True,
                           unique=True, nullable=False)
    user_password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey(
        'role.role_id', onupdate="CASCADE", ondelete="SET NULL"), nullable=True)

    user_pages = db.relationship('Page', backref='page_author', lazy='dynamic')

    def __repr__(self):
        return self.user_login

    def get_id(self):
        return str(self.user_id)

    @hybrid_property
    def user_password(self):
        return ''

    @user_password.setter
    def user_password(self, new_user_password):
        if new_user_password:
            self.user_password_hash = generate_password_hash(new_user_password)

    def verify_password(self, password):
        return check_password_hash(self.user_password_hash, password)


# Menu


menu_page = db.Table(
    'menu_page',
    db.Column('item_id', db.Integer, db.ForeignKey(
        'menu_item.item_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('page_id', db.Integer, db.ForeignKey(
        'page.page_id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
    db.PrimaryKeyConstraint('item_id')
)

menu_link = db.Table(
    'menu_link',
    db.Column('item_id', db.Integer, db.ForeignKey(
        'menu_item.item_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('link_id', db.Integer, db.ForeignKey(
        'link.link_id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
    db.PrimaryKeyConstraint('item_id')
)

class MenuItem(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(32), index=True,
                          unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey(
        'menu_item.item_id', onupdate="CASCADE", ondelete="SET NULL"), nullable=True)


    item_subitems = db.relationship(
        'MenuItem', backref=db.backref("item_parent", remote_side=item_id), lazy='dynamic')

    item_link = db.relationship(
        'Link', lazy='joined', secondary=menu_link, backref='menu_item', uselist=False)
    item_page = db.relationship(
        'Page', lazy='joined', secondary=menu_page, backref='menu_item', uselist=False)

    def __repr__(self):
        return self.item_name


class Link(db.Model):
    link_id = db.Column(db.Integer, primary_key=True)
    link_url = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return self.link_url

# Tags


page_tag = db.Table(
    'page_tag',
    db.Column('page_id', db.Integer, db.ForeignKey(
        'page.page_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('tag_id', db.Integer, db.ForeignKey(
        'tag.tag_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.PrimaryKeyConstraint('page_id', 'tag_id')
)


class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(32), index=True,
                         unique=True, nullable=False)

    def __repr__(self):
        return self.tag_name


# Files

page_file = db.Table(
    'page_file',
    db.Column('page_id', db.Integer, db.ForeignKey(
        'page.page_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('file_id', db.Integer, db.ForeignKey(
        'file.file_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.PrimaryKeyConstraint('page_id', 'file_id')
)


class File(db.Model):
    file_id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return self.file_name


# pages

class Page(db.Model):
    page_id = db.Column(db.Integer, primary_key=True)
    page_title = db.Column(db.String(64), index=True,
                           unique=True, nullable=False)
    page_url = db.Column(db.String(64), unique=True, nullable=False)
    page_timestamp = db.Column(
        db.DateTime, index=True, default=datetime.utcnow, nullable=True)
    page_visible = db.Column(db.Boolean, index=True,
                             default=True, nullable=False)
    page_preview = db.Column(db.Text, nullable=True)
    page_content = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True)

    page_tags = db.relationship(
        'Tag', lazy='dynamic', secondary=page_tag, backref='tag_pages')
    page_files = db.relationship(
        'File', lazy='dynamic', secondary=page_file, backref='file_pages')

    def __repr__(self):
        return self.page_title

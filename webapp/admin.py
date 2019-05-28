from flask_admin.contrib.sqla import ModelView
from flask import url_for, redirect, request, flash
from webapp import dashboard
from webapp.models import *
from webapp.validators import *
from wtforms import fields, widgets
from wtforms.fields import PasswordField
from wtforms.validators import *
from flask_login import current_user
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import form
from flask_admin.menu import MenuLink
from sqlalchemy.event import listens_for
import os.path as op
import os

unmanaged_path = op.join(op.dirname(__file__), 'static', 'files')
managed_path = op.join(op.dirname(__file__), 'static', 'managed')

try:
    os.mkdir(unmanaged_path)
except OSError:
    pass

try:
    os.mkdir(managed_path)
except OSError:
    pass


def has_permission(id):
        return bool(current_user.user_role.role_perms.filter_by(perm_id=id).first())


class ProtectedView(ModelView):
    def is_accessible(self):
        return has_permission(1)

    def inaccessible_callback(self, name, **kwargs):
        # redirect to admin page if user doesn't have access
        return redirect(url_for('admin', next=request.url))

    create_modal = True
    edit_modal = True


class UtilityView(ProtectedView):
    def is_accessible(self):
        return super().is_accessible() or has_permission(2)


class ManageUsersView(ProtectedView):
    def is_accessible(self):
        return super().is_accessible() or has_permission(3)


class StructureView(ProtectedView):
    def is_accessible(self):
        return super().is_accessible() or has_permission(4)


class ContentView(ProtectedView):
    def is_accessible(self):
        return super().is_accessible() or has_permission(5)


class ProtectedFileAdmin(FileAdmin):
    def is_accessible(self):
        return has_permission(1) or has_permission(2)

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('admin', next=request.url))


class UserView(ManageUsersView):
    column_exclude_list = ['user_password_hash']
    column_searchable_list = ['user_login']
    column_editable_list = ['user_login']

    column_list = ['user_login', 'user_role']
    column_default_sort = ('role_id', True)

    form_excluded_columns = ['user_pages', 'user_password_hash']

    form_args = dict(
        user_login=dict(validators=[username_validator])
    )

    form_extra_fields = {
        'password': PasswordField('Password', [
            Optional(),
            EqualTo('confirm', message='Passwords must match'),
            password_validator]),
        'confirm': PasswordField('Repeat Password')
    }

    def on_model_change(self, form, model, is_created):
        if is_created and not form.password.data:
            raise ValidationError("User can't have empty password!")
        if form.password.data:
            model.user_password = form.password.data


class RoleView(ManageUsersView):
    column_searchable_list = ['role_name']
    column_editable_list = ['role_name']

    form_excluded_columns = ['role_users']


class PermView(UtilityView):
    column_display_pk = True
    column_searchable_list = ['perm_name']
    can_delete = False
    can_create = False
    can_edit = False

    column_default_sort = ('perm_id', False)
    form_excluded_columns = ['perm_roles']


class MenuView(StructureView):
    column_display_pk = True
    column_searchable_list = ['item_name']
    column_editable_list = ['item_name']

    column_default_sort = ('item_id', False)

    def on_model_change(self, form, model, is_created):
        if form.item_link.data and form.item_page.data:
            raise ValidationError("Menu item can't be attached both to page and static link!")
        if form.item_parent.data == model or form.item_subitems.data.count(model):
            raise ValidationError("Menu item can't be a parent of itself!")


class LinkView(StructureView):
    column_searchable_list = ['link_url']
    column_editable_list = ['link_url']


class TagView(ContentView):
    column_searchable_list = ['tag_name']
    column_editable_list = ['tag_name']

    column_default_sort = ('tag_name', True)


class MDETextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        # add WYSIWYG class to existing classes
        existing_classes = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = '{} {}'.format(existing_classes, "simplemde")
        return super(MDETextAreaWidget, self).__call__(field, **kwargs)


class MDETextAreaField(fields.TextAreaField):
    widget = MDETextAreaWidget()


class PageView(ContentView):
    column_searchable_list = ['page_title', 'page_preview', 'page_content', 'page_author.user_login']
    column_editable_list = ['page_title', 'page_url', 'page_visible']
    column_exclude_list = ['page_content']


    column_default_sort = ('page_timestamp', True)

    create_modal = False
    edit_modal = False

    form_args = dict(
        page_url=dict(validators=[slug_validator]),
        page_author=dict(default=lambda _: current_user)
    )

    form_columns = [
        'page_title',
        'page_url',
        'page_author',
        'page_timestamp',
        'page_visible',
        'page_preview',
        'page_content',
        'page_files',
        'page_tags'
    ]

    form_overrides = {
        'page_content': MDETextAreaField,
        'page_preview': MDETextAreaField
    }

    create_template = 'create_page.html'
    edit_template = 'edit_page.html'

    def create_form(self):
        form = super(PageView, self).create_form()
        form.page_author.data = current_user
        return form


class FileView(ContentView):
    column_searchable_list = ['file_path']
    can_edit = False

    form_overrides = {
        'file_path': form.FileUploadField
    }

    # Pass additional parameters to 'path' to FileUploadField constructor
    form_args = {
        'file_path': {
            'label': 'File',
            'base_path': managed_path,
            'allow_overwrite': False
        }
    }


@listens_for(File, 'after_delete')
def del_file(mapper, connection, target):
    if target.file_path:
        try:
            os.remove(op.join(managed_path, target.file_path))
        except OSError:
            pass

dashboard.add_link(MenuLink(name='Back to site', url='/'))

dashboard.add_view(PageView(Page, db.session, category="Content"))
dashboard.add_view(TagView(Tag, db.session, category="Content"))
dashboard.add_view(FileView(File, db.session, category="Content"))

dashboard.add_view(MenuView(MenuItem, db.session, category="Structure"))
dashboard.add_view(LinkView(Link, db.session, category="Structure"))

dashboard.add_view(UserView(User, db.session, category="User Management"))
dashboard.add_view(RoleView(Role, db.session, category="User Management"))
dashboard.add_view(PermView(Perm, db.session, category="Utilities"))

dashboard.add_view(ProtectedFileAdmin(unmanaged_path, '/static/files/', name='Static Files', category="Utilities"))

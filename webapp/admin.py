from flask_admin.contrib.sqla import ModelView
from webapp import dashboard
from webapp.models import *
from wtforms import fields, widgets
from wtforms.fields import PasswordField
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import form
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


class UserView(ModelView):
    column_exclude_list = ['user_password_hash']
    column_searchable_list = ['user_login']
    column_editable_list = ['user_login']

    create_modal = True
    edit_modal = True

    form_excluded_columns = ['user_pages', 'user_password_hash']

    form_extra_fields = {
        'password': PasswordField('Password')
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.user_password = form.password.data


class RoleView(ModelView):
    column_searchable_list = ['role_name']
    column_editable_list = ['role_name']

    create_modal = True
    edit_modal = True

    form_excluded_columns = ['role_users']


class PermView(ModelView):
    column_searchable_list = ['perm_name']
    column_editable_list = ['perm_name']

    create_modal = True
    edit_modal = True

    form_excluded_columns = ['perm_roles']


class MenuView(ModelView):
    column_display_pk = True
    column_searchable_list = ['item_name']
    column_editable_list = ['item_name']

    create_modal = True
    edit_modal = True


class LinkView(ModelView):
    column_searchable_list = ['link_url']
    column_editable_list = ['link_url']

    create_modal = True
    edit_modal = True


class TagView(ModelView):
    column_searchable_list = ['tag_name']
    column_editable_list = ['tag_name']

    create_modal = True
    edit_modal = True


class MDETextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        # add WYSIWYG class to existing classes
        existing_classes = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = '{} {}'.format(existing_classes, "simplemde")
        return super(MDETextAreaWidget, self).__call__(field, **kwargs)


class MDETextAreaField(fields.TextAreaField):
    widget = MDETextAreaWidget()


class PageView(ModelView):
    column_searchable_list = ['page_title', 'page_preview', 'page_content']
    column_editable_list = ['page_title', 'page_url']
    column_exclude_list = ['page_content']

    form_overrides = {
        'page_content': MDETextAreaField,
        'page_preview': MDETextAreaField
    }

    create_template = 'create_page.html'
    edit_template = 'edit_page.html'


class FileView(ModelView):
    column_searchable_list = ['file_path']
    create_modal = True
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


dashboard.add_view(PageView(Page, db.session))
dashboard.add_view(TagView(Tag, db.session))
dashboard.add_view(FileView(File, db.session))

dashboard.add_view(MenuView(MenuItem, db.session))
dashboard.add_view(LinkView(Link, db.session))

dashboard.add_view(UserView(User, db.session))
dashboard.add_view(RoleView(Role, db.session))
dashboard.add_view(PermView(Perm, db.session))

dashboard.add_view(FileAdmin(unmanaged_path, '/static/files/', name='Static Files'))

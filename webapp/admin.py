from flask_admin.contrib.sqla import ModelView
from webapp import dashboard
from webapp.models import *
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


class FileView(ModelView):

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


dashboard.add_view(UserView(User, db.session))
dashboard.add_view(RoleView(Role, db.session))
dashboard.add_view(ModelView(Perm, db.session))  # comment out
dashboard.add_view(FileView(File, db.session))
dashboard.add_view(ModelView(MenuItem, db.session))


unmanaged_path = op.join(op.dirname(__file__), 'static', 'files')
dashboard.add_view(FileAdmin(unmanaged_path, '/static/files/', name='Static Files'))

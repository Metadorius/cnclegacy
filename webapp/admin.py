from flask_admin.contrib.sqla import ModelView
from webapp import dashboard
from webapp.models import *
from wtforms.fields import PasswordField


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


dashboard.add_view(UserView(User, db.session))

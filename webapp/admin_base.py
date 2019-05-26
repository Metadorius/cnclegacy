from flask import request, redirect, url_for
from flask_login import current_user
from flask_admin import AdminIndexView, expose


class ProtectedAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login', next=request.url))
        return redirect(self.get_url('page.index_view', search=current_user.user_login))

from flask import request, redirect, url_for
from flask_login import current_user
from flask_admin import AdminIndexView, expose


class ProtectedAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login', next=request.url))
        return super(ProtectedAdminIndexView, self).index()

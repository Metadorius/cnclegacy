from flask_admin.contrib.sqla import ModelView
from webapp import dashboard
from webapp.models import *

dashboard.add_view(ModelView(User, db.session))
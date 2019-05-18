from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from webapp.admin_base import ProtectedAdminIndexView


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
dashboard = Admin(app, name='Dashboard', index_view=ProtectedAdminIndexView())
bootstrap = Bootstrap(app)


from webapp import routes, models, admin, errors

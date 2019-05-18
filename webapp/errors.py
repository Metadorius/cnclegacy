from flask import render_template
from webapp import app, db
from webapp.models import *


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', menu_items=MenuItem.query.filter_by(parent_id=None).all()), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', menu_items=MenuItem.query.filter_by(parent_id=None).all()), 500

from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app.classes.data import require_role,Role,User
import datetime as dt

@app.route('/admintest')
@require_role('admin')
def admintest():
    if current_user.has_role('admin'):
        flash('You have the Admin role.')
    return redirect('/')

@app.route('/listroles')
@require_role('admin')
def listroles():
    roles = Role.objects()
    for role in roles:
        flash(role.name)
    return render_template('index.html')


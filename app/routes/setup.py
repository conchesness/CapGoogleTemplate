from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app.classes.data import require_role, Role, User
import datetime as dt

# if you ever host this site so that it can be accessed on the web you should comment out these routes.

@app.route('/makerole/<name>')
@login_required
def makeroles(name):

    name=name.lower()

    try:
        Role(name=name).save()
    except mongoengine.errors.NotUniqueError:
        flash(f"{name} Role already exists")
    else:
        flash(f'{name} Role created.')

    return render_template('index.html')

@app.route('/addroletouser/<email>/<rolename>')
@login_required
def addroletouser(email,rolename):

    rolename=rolename.lower()

    try:
        role = Role.objects.get(name=rolename)
    except mongoengine.errors.DoesNotExist:
        flash(f'The role {role.name} does not exist.')
        return redirect("/")

    try:
        user = User.objects.get(email=email)
    except mongoengine.errors.DoesNotExist:
        flash("That user doesn't exist")
    else:
        if user.has_role(role.name):
            flash(f'{user.fname} {user.lname} already has the role {role.name}.')
            return redirect("/")
        user.roles.append(role)
        user.save()
        flash(f"{user.fname} {user.lname} is now has the role {role.name}.")

    return redirect("/")
# This is where all the database collections are defined. A collection is a place to hold a defined 
# set of data like Users, Blogs, Comments. Collections are defined below as classes. Each class name is 
# the name of the data collection and each item is a data 'field' that stores a piece of data.  Data 
# fields have types like IntField, StringField etc.  This uses the Mongoengine Python Library. When 
# you interact with the data you are creating an onject that is an instance of the class.

from sys import getprofile
from tokenize import String
from typing import KeysView
from xmlrpc.client import Boolean

from setuptools import SetuptoolsDeprecationWarning
from app import app
from flask import flash, redirect
from flask_login import UserMixin, current_user
from mongoengine import Document, ListField, FileField, EmailField, StringField, IntField, ReferenceField, DateTimeField, BooleanField, FloatField, CASCADE
import datetime as dt
import jwt
from time import time
from bson.objectid import ObjectId
from flask_security import RoleMixin
from functools import wraps


class User(UserMixin, Document):
    createdate = DateTimeField(defaultdefault=dt.datetime.utcnow)
    gid = StringField(sparse=True, unique=True)
    gname = StringField()
    gprofile_pic = StringField()
    username = StringField()
    fname = StringField()
    lname = StringField()
    email = EmailField()
    image = FileField()
    prononuns = StringField()
    roles = ListField(ReferenceField("Role"))

    meta = {
        'ordering': ['lname','fname']
    }

    def has_role(self, name):
        """Does this user have this permission?"""
        try:
            chk_role = Role.objects.get(name=name)
        except:
            flash(f"{name} is not a valid role.")
            return False
        if chk_role in self.roles:
            return True
        else:
            flash(f"That page requires the {name} role.")
            return False

class Role(RoleMixin, Document):
    # The RoleMixin requires this field to be named "name"
    name = StringField(unique=True)

# To require a role for a specific route use this decorator
# @require_role(role="student")

def require_role(role):
    """make sure user has this role"""
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            if not current_user.has_role(role):
                return redirect("/")
            else:
                return func(*args, **kwargs)
        return wrapped_function
    return decorator

class Blog(Document):
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    subject = StringField()
    content = StringField()
    tag = StringField()
    create_date = DateTimeField(default=dt.datetime.utcnow)
    modify_date = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }

class Comment(Document):
    # Line 63 is a way to access all the information in Course and Teacher w/o storing it in this class
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    blog = ReferenceField('Blog',reverse_delete_rule=CASCADE)
    # This could be used to allow comments on comments
    comment = ReferenceField('Comment',reverse_delete_rule=CASCADE)
    # Line 68 is where you store all the info you need but won't find in the Course and Teacher Object
    content = StringField()
    create_date = DateTimeField(default=dt.datetime.utcnow)
    modify_date = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }

class Clinic(Document):
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    createdate = DateTimeField(default=dt.datetime.utcnow)
    modifydate = DateTimeField()
    name = StringField()
    streetAddress = StringField()
    city = StringField()
    state = StringField()
    zipcode = StringField()
    description = StringField()
    lat = FloatField()
    lon = FloatField()
    
    meta = {
        'ordering': ['-createdate']
    }


# Events are items that are displayed on the calendar.  The fields are very simple and
# and can easily be changed to add other information that you want. 
class Event(Document):
    # All events have 'owners' which are a referencefield connected to the User document
    owner = ReferenceField(User)
    title = StringField()
    desc = StringField()
    date = DateTimeField()

    meta = {
        'ordering': ['+date']
    }
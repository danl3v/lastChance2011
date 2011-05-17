from google.appengine.ext import db
from google.appengine.api import users

class Carl(db.Model):
    googleID = db.StringProperty() # change to underscores
    carletonID = db.StringProperty()
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    pair_code = db.StringProperty() # set default to generateVerificationCode?
    opted_in = db.BooleanProperty(default=True)

class Crush(db.Model):
    source = db.ReferenceProperty(Carl, collection_name="crush_source")
    target = db.ReferenceProperty(Carl, collection_name="crush_target")

class Thread(db.Model):
    deleted = db.BooleanProperty(default=False) 
    source = db.ReferenceProperty(Carl, collection_name="thread_source")
    target = db.ReferenceProperty(Carl, collection_name="thread_target")
    message = db.StringProperty(multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)
from google.appengine.ext import db
from google.appengine.api import users

class Carl(db.Model):
    googleID = db.StringProperty() # change to underscores
    carletonID = db.StringProperty()
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    verificationCode = db.StringProperty() # set default to generateVerificationCode?
    active = db.BooleanProperty(default=True) # if the user opts out, this is set to false

class Carl2Carl(db.Model): # change to crush
    source = db.StringProperty() # change to reference properties
    target = db.StringProperty()

class Message(db.Model):
    deleted = db.BooleanProperty(default=False) 
    source = db.StringProperty() # change to reference properties
    target = db.StringProperty()
    message = db.StringProperty(multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)

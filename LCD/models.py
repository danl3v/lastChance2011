from google.appengine.ext import db

class Carl(db.Model):
    googleID = db.StringProperty()
    carletonID = db.StringProperty()
    verificationCode = db.StringProperty()

class Carl2Carl(db.Model):
    source = db.StringProperty()
    target = db.StringProperty()

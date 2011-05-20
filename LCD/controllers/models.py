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

class Message(db.Model): # change this back to message
    source = db.ReferenceProperty(Carl, collection_name="in_messages")
    target = db.ReferenceProperty(Carl, collection_name="out_messages")
    source_deleted = db.BooleanProperty(default=False)
    target_deleted = db.BooleanProperty(default=False)

    body = db.StringProperty(multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now_add=True)
    
    @property
    def replies(self):
        return Reply.gql("WHERE message = :1 ORDER BY created ASC", self.key())

class Reply(db.Model):
    message = db.ReferenceProperty(Message, collection_name="reply_message")
    source = db.ReferenceProperty(Carl, collection_name="reply_source")
    body = db.StringProperty(multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)

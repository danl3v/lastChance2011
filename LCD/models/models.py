from google.appengine.ext import db
from google.appengine.api import users
from datetime import timedelta
tz_offset = -5

class Setting(db.Model):
    name = db.StringProperty()
    value = db.StringProperty()
    
class Statistic(db.Model):
    name = db.StringProperty()
    value = db.IntegerProperty()

class Carl(db.Model):
    googleID = db.StringProperty(default=None) # change to underscores
    carletonID = db.StringProperty()
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    pair_code = db.StringProperty() # set default to generateVerificationCodeed
    opted_in = db.BooleanProperty(default=True)

    has_unread_messages = db.BooleanProperty(default=False)
        
    @property
    def matches(self):
        return Match.gql("WHERE source = :1", self.key())

class Crush(db.Model):
    source = db.ReferenceProperty(Carl, collection_name="in_crushes")
    target = db.ReferenceProperty(Carl, collection_name="out_crushes")
    notified = db.BooleanProperty(default=False)
    
class Match(db.Model):
    source = db.ReferenceProperty(Carl, collection_name="in_matches")
    target = db.ReferenceProperty(Carl, collection_name="out_matches")

class Message(db.Model):
    source = db.ReferenceProperty(Carl, collection_name="in_messages")
    target = db.ReferenceProperty(Carl, collection_name="out_messages")
    source_deleted = db.BooleanProperty(default=False)
    target_deleted = db.BooleanProperty(default=False)

    body = db.StringProperty(multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now_add=True)

    unread = db.BooleanProperty(default=True)
    
    @property
    def local_created(self):
        return self.created + timedelta(hours=tz_offset)
        
    @property
    def local_updated(self):
        return self.updated + timedelta(hours=tz_offset)
    
    @property
    def replies(self):
        return Reply.gql("WHERE message = :1 ORDER BY created ASC", self.key())

class Reply(db.Model):
    message = db.ReferenceProperty(Message, collection_name="reply_message")
    source = db.ReferenceProperty(Carl, collection_name="reply_source")
    body = db.StringProperty(multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)

    unread = db.BooleanProperty(default=True)
    
    @property
    def local_created(self):
        return self.created + timedelta(hours=tz_offset)

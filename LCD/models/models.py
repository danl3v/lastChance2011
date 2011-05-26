from google.appengine.ext import db
from datetime import timedelta, datetime
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

    num_unread_messages = db.IntegerProperty(default=0)
    num_unread_sent_messages = db.IntegerProperty(default=0)
        
class Crush(db.Model):
    source = db.ReferenceProperty(Carl, collection_name="in_crushes")
    target = db.ReferenceProperty(Carl, collection_name="out_crushes")
    created = db.DateTimeProperty(auto_now_add=True)
    deleted = db.BooleanProperty(default=False)
    deleted_time = db.DateTimeProperty(auto_now_add=False)
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

    target_unread = db.BooleanProperty(default=True)

    source_any_unread = db.BooleanProperty(default=False)
    target_any_unread = db.BooleanProperty(default=True)

    @property
    def local_created(self): return self.created + timedelta(hours=tz_offset)
    
    @property
    def pretty_created(self): return pretty_date(self, self.created)
    
    @property
    def local_updated(self): return self.updated + timedelta(hours=tz_offset)

    def pretty_updated(self): return pretty_date(self, self.updated)
    
class Reply(db.Model):
    message = db.ReferenceProperty(Message, collection_name="reply_messages")
    source = db.ReferenceProperty(Carl, collection_name="reply_source")
    body = db.StringProperty(multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)

    source_unread = db.BooleanProperty(default=True)
    target_unread = db.BooleanProperty(default=True)

    @property
    def local_created(self): return self.created + timedelta(hours=tz_offset)

    @property
    def pretty_created(self): return pretty_date(self, self.created)

def pretty_date(self, time):
    now = datetime.now()
    diff = now - time 
    second_diff = diff.seconds
    day_diff = diff.days
    if day_diff < 0: return ""
    if day_diff == 0:
        if second_diff < 10: return "just now"
        if second_diff < 60: return str(second_diff) + " seconds ago"
        if second_diff < 120: return  "a minute ago"
        if second_diff < 3600: return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200: return "an hour ago"
        if second_diff < 86400: return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1: return "Yesterday at " + self.local_updated.strftime("%I:%M%p")
    if day_diff < 7: return self.local_updated.strftime("%A at %I:%M%p")
    if day_diff < 365: return self.local_updated.strftime("%B %d at %I:%M%p")
    return self.local_updated.strftime("%B %d, %Y at %I:%M%p")

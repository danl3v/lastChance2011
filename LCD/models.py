from google.appengine.ext import db
from google.appengine.api import users

# What the data looks like:

class Carl(db.Model): #add first name and last name for autocomplete
    googleID = db.StringProperty()
    carletonID = db.StringProperty()
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    verificationCode = db.StringProperty() # set default to generateVerificationCode?
    active = db.BooleanProperty(default=True) # if the user opts out, this is set to false

class Carl2Carl(db.Model):
    source = db.StringProperty()
    target = db.StringProperty()

#class Crush(db.Model):
#    source = db.ReferenceProperty(Carl);
#    target = db.ReferenceProperty(Carl);

class Message(db.Model):
    deleted = db.BooleanProperty(default=False) 
    source = db.StringProperty()  # hash(Carl.carletonID)
    target = db.StringProperty()  # Carl.carletonID
    message = db.StringProperty(multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)

### Get stuff from the Database ###

def get_crushes_for_user(user):
    carl2carl = Carl2Carl.all()
    carl2carl.filter("source =", user)
    results = carl2carl.fetch(20) # there should not be more than 5
    return [get_user_by_CID(result.target) for result in results]

def get_crushes_for_user_by_target(user):
    carl2carl = Carl2Carl.all()
    carl2carl.filter("target =", user)
    results = carl2carl.fetch(1000) # there should not be more than num users in db
    return [get_user_by_CID(result.source) for result in results]

def has_crush(source, target):
    carl2carl = Carl2Carl.all()
    carl2carl.filter("source =", source)
    carl2carl.filter("target =", target)
    carl = carl2carl.get()
    return carl

def get_user_by_CID(username):
    carl = Carl.all()
    carl.filter("carletonID =",username)
    return carl.get()

def get_messages_by_CID(carleton_id):
    messages = Message.all()
    messages.filter("target =", carleton_id)
    messages.filter("deleted =", False)
    messages.order("-created")
    return messages.fetch(1000)

def generate_pair_code():
    import random, string
    N = 20
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))

def calculate_matches():
    crushes = Carl2Carl.all()
    return [(crush.source, crush.target) for crush in crushes if has_crush(crush.target, crush.source)]

def num_crushes():
    return Carl2Carl.all().count()

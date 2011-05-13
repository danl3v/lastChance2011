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

class Message(db.Model):
    deleted = db.BooleanProperty(default=False) 
    source = db.StringProperty()  # hash(Carl.carletonID)
    target = db.StringProperty()  # Carl.carletonID
    message = db.StringProperty(multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)

### Get stuff from the Database ###

# rename get_crushes_for_user
def getCarlCrushes(user): # do a join in here so we can get usernames too
    carl2carl = Carl2Carl.all()
    carl2carl.filter("source =", user)
    results = carl2carl.fetch(20) # there should not be more than 5
    return [get_user_by_CID(result.target) for result in results]

#rename has_crush
def hasCrush(source, target):
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

# rename generate_verification_code
def generateVerificationCode():  # maybe this is more of a 'controller' function
    import random, string
    N = 20
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))

# def calculate_matches()

# def num_matches()

def num_crushes():
    return Carl2Carl.all().count()

# def num_active_users()

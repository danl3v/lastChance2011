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
    read = db.BooleanProperty() 
    source = db.StringProperty()  # hash(Carl.carletonID)
    target = db.StringProperty()  # Carl.carletonID
    message = db.StringProperty(multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)

### Get stuff from the Database ###

def getCarlCrushes(user): # do a join in here so we can get usernames too
    # returns carl2carl model instances for a given user's preferences
    carl2carl = Carl2Carl.all()
    carl2carl.filter("source =", user)
    results = carl2carl.fetch(20) # there should not be more than 5
    preferences = [] if results is None else results  # type checking if there's no preferences in DB
    return preferences

def get_user_by_CID(username):
    '''
    returns a user row given their carleton id
    '''
    carl = Carl.all()
    carl.filter("carletonID =",username)
    return carl.get()

def get_messages_by_CID(carleton_id):
    messages = Message.all()
    messages.filter("target =", carleton_id)
    #messages.order("-created") # we want to sort the messages my date

    return messages.fetch(1000)

def generateVerificationCode():  # maybe this is more of a 'controller' function
    import random, string
    N = 20
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))

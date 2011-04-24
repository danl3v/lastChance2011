from google.appengine.ext import db
from google.appengine.api import users

# What the data looks like:

class Carl(db.Model):
    googleID = db.StringProperty()
    carletonID = db.StringProperty()
    verificationCode = db.StringProperty() # set default to generateVerificationCode?
    active = db.BooleanProperty(default=True) # if the user opts out, this is set to false

# Might want to put "isPaired" here?
# the function for seeing if the session user has paired their account is both a model and a session-based peice of code. tricky to find its home

class Carl2Carl(db.Model):
    source = db.StringProperty()
    target = db.StringProperty()

class Message(db.Model):
    target = db.StringProperty()
    message = db.StringProperty()


# Things that access data, either from the session or the database

### Get stuff from the Database ###


def getCarlCrushes(user):
    # returns carl2carl model instances for a given user's preferences
    carl2carl = Carl2Carl.all()
    carl2carl.filter("source =", user)
    results = carl2carl.fetch(20)
    preferences = [] if results is None else results  # type checking if there's no preferences in DB
    return preferences

def get_user_by_CID(username):
    '''
    returns a user row given their carleton id
    '''
    carl = Carl.all()
    carl.filter("carletonID =",username)
    return carl.get()


### Other ###

def generateVerificationCode():  # maybe this is more of a 'controller' function
    # Dumb for now - make it a random string or something in the future
    return "apples"

from google.appengine.ext import db
from google.appengine.api import users

# What the data looks like:

class Carl(db.Model):
    googleID = db.StringProperty()
    carletonID = db.StringProperty()
    verificationCode = db.StringProperty()

class Carl2Carl(db.Model):
    source = db.StringProperty()
    target = db.StringProperty()

# Things that access data, either from the session or the database

### Get info about the current user ####
## Maybe this should be in a /sessionfunctions.py thing in case
## we wanna change from google

def isPaired():
    carl = Carl.all()
    carl.filter("googleID =", str(users.get_current_user().user_id()))
    count = carl.count()
    if count == 0:
        return False
    elif count == 1:
        return True

def getCarl(): 
    carl = Carl.all()
    carl.filter("googleID =", str(users.get_current_user().user_id()))
    return carl.get()

def getCarlPreferences(user):
    carl2carl = Carl2Carl.all()
    carl2carl.filter("source =", user)
    results = carl2carl.fetch(20)
    return results

### Get stuff from the Database ###

def get_user_by_CID(username):
    '''
    returns a user row given their carleton id
    '''
    carl = Carl.all()
    carl.filter("carletonID =",username)
    return carl.get()


### Other ###

def generateVerificationCode():  # maybe this is more of a 'controller' function
    # Dumb for now
    return "apples"

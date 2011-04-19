from models import *
from google.appengine.api import users

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

def get_user_by_CID(username):
    '''
    returns a user row given their carleton id
    '''
    carl = Carl.all()
    carl.filter("carletonID =",username)
    return carl.get()

def generateVerificationCode():
    # Dumb for now
    return "apples"

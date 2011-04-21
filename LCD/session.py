from google.appengine.api import users
import models


def get_current_user():
    return users.get_current_user()

def create_logout_url(theURI):
    return users.create_logout_url(theURI)

def create_login_url(theURI):
    return users.create_login_url(theURI)

def is_current_user_admin():
    return users.is_current_user_admin()

### Get info about the current user ####
## Maybe this should be in a /sessionfunctions.py thing in case
## we wanna change from google

def isPaired():
    '''
    returns True if current user is paired with a carleton account, False otherwise
    '''
    carl = models.Carl.all()
    carl.filter("googleID =", str(users.get_current_user().user_id()))
    count = carl.count()

    assert count in [0,1], "this google account is paired with more than one carleton account"

    if count == 0: return False
    elif count == 1: return True

def is_active():
    '''
    returns True if current user is active, False if current user us not active or if account not paired
    '''
    carl = getCarl()
    return carl.active if carl else False

def getCarl(): 
    carl = models.Carl.all()
    carl.filter("googleID =", str(users.get_current_user().user_id()))
    return carl.get()


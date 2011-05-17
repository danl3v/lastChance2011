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

    return count # 1 if paired, 0 if not paired

def opted_in():
    '''
    returns True if current user is opted_in, False if current user is not opted_in or if account not paired
    '''
    carl = getCarl()
    return carl.opted_in if carl else False

def getCarl(): 
    """crashes if run on anonymous sessions"""
    carl = models.Carl.all()
    carl.filter("googleID =", str(users.get_current_user().user_id()))
    return carl.get()



from google.appengine.api import users


def get_current_user():
    return users.get_current_user()

def create_logout_url(theURI):
    return users.create_logout_url(theURI)

def create_login_url(theURI):
    return users.create_login_url(theURI)

def is_current_user_admin():
    return users.is_current_user_admin()

import cgi
import os

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

#### FUNCTIONS ####

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

def getPerson(username):  # Need your advice, dan
    carl = Carl.all()
    carl.filter("carletonID =",username)
    return carl.get()

def generateVerificationCode():
    # Dumb for now
    return "apples"

#### MODELS ####

class Carl(db.Model):
    googleID = db.StringProperty()
    carletonID = db.StringProperty()
    verificationCode = db.StringProperty()

class Carl2Carl(db.Model):
    source = db.StringProperty()
    target = db.StringProperty()    

#### CONTROLLERS #####

class MainPage(webapp.RequestHandler):
    def get(self):

        user = users.get_current_user()
        if user:
            login_url = users.create_logout_url(self.request.uri)
            login_url_linktext = 'Logout'
            
            if isPaired():
                pair_url = "pair"
                pair_url_linktext = "Unpair Your Account"
            else:
                pair_url = "pair"
                pair_url_linktext = "You need to pair your account"
        else:
            login_url = users.create_login_url(self.request.uri)
            login_url_linktext = 'Login'
            pair_url = ""
            pair_url_linktext = ""

  
        if users.is_current_user_admin():
            admin = True
        else:
            admin = False

        template_values = {
            'user': user,
            'admin': admin,
            'login_url': login_url,
            'login_url_linktext': login_url_linktext,
            'pair_url': pair_url,
            'pair_url_linktext': pair_url_linktext
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, template_values))

class Pair(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'templates/pair.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        if isPaired():
            # use get() to return the carleton email id that this google account was paired to
            self.response.out.write("Your account is already paired")
        else:
            #theCarl = Carl().all()
            #theCarl.filter("carletonID =",self.request.get('carletonID'))
            theCarl = getPerson(self.request.get('carletonID'))
            self.response.out.write(theCarl.carletonID)
            self.response.out.write(theCarl.verificationCode)
            # uhh.. this better only be one entry.
            if theCarl.verificationCode == self.request.get('verificationCode'):
                theCarl.googleID = str(users.get_current_user().user_id())
                theCarl.verificationCode = ""
                theCarl.put()
                self.response.out.write("Your account was successfully paired:<br>")
                self.response.out.write("Carleton ID:" + theCarl.carletonID + "<br>")
                self.response.out.write("GoogleID: " + theCarl.googleID)

class Admin(webapp.RequestHandler):
    def get(self):
        carls = Carl.all()
        template_values = {
            'carls' : carls
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/admin.html')
        self.response.out.write(template.render(path, template_values))

class AddCarl(webapp.RequestHandler):  # Adding a new student to database
    def post(self):
        if users.is_current_user_admin():
            from random import randint
            admin = True
            carl = Carl()
            carl.carletonID = self.request.get('carletonID')
            carl.verificationCode = str(randint(0,2**16))
            self.response.out.write('Trying to put '+carl.carletonID+' into database.')
            carl.put()
            self.redirect('/admin')
        else:
            admin = False
            self.response.out.write('Hey! You are not an administrator. SHAME')


class PairCode(webapp.RequestHandler):
    def post(self):
        self.response.out.write(self.request.get('carletonID'))
        # Lookup carletonID -> get/generate verification code
        carletonAccount = getPerson(self.request.get('carletonID'))
        carletonAccount.verificationCode = generateVerificationCode()
        carletonAccount.put()
        # mail some stuff
        '''http://code.google.com/appengine/docs/python/mail/sendingmail.html'''
        self.response.out.write("<br>Your pair code has been sent!! jk. we haven't coded that much yet.")

class Preferences(webapp.RequestHandler):
    def get(self):

        carl2carl = Carl2Carl.all()
        carl2carl.filter("source =", getCarl().carletonID)
        results = carl2carl.fetch(20)
        used_spots = carl2carl.count()

        total_spots = 10 # this is the number of people someone can select
        remaining_spots = total_spots - used_spots
        if remaining_spots < 1: remaining_spots = 0

        template_values = {
            'carls': results,
            'n': range(remaining_spots)
            }

        path = os.path.join(os.path.dirname(__file__), 'preferences.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        carls = self.request.getall('new_carl') #having some issues here with getting values of text boxes
        # save the prefs here
        for carl in carls:
            self.response.out.write(carl + "<br>")

        #self.redirect("/preferences")


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/admin', Admin),
                                      ('/admin/addcarl', AddCarl),
                                      ('/preferences', Preferences),
                                      ('/pair', Pair),
                                      ('/sendPairCode', PairCode)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

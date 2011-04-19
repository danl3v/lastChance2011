import cgi
import os

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models 
from functions import *

import mailfunction

class MainPage(webapp.RequestHandler):
    def get(self):

        user = users.get_current_user()
        if user:
            login_url = users.create_logout_url(self.request.uri)
            login_url_linktext = 'Logout'
            
            if models.isPaired():
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
        if models.isPaired():
            # use get() to return the carleton email id that this google account was paired to
            self.response.out.write("Your account is already paired")
        else:
            theCarl = models.get_user_by_CID(self.request.get('carletonID'))
            if theCarl.verificationCode == self.request.get('verificationCode'):
                theCarl.googleID = str(users.get_current_user().user_id())
                theCarl.verificationCode = "" # yeah, what do we want to do with this field? should we keep the verification code there?
                theCarl.put()
                self.response.out.write("Your account was successfully paired:<br>")
                self.response.out.write("Carleton ID :" + theCarl.carletonID + "<br>")
                self.response.out.write("GoogleID: " + theCarl.googleID)
            else:
                self.response.out.write("You entered an incorrect verification code")
                self.response.out.write("Carleton ID:" + theCarl.carletonID)
                self.response.out.write("Google ID: " + str(users.get_current_user().user_id()))
                self.response.out.write("Verification Code:" + theCarl.verificationCode)

class PairCode(webapp.RequestHandler):
    def post(self):
        self.response.out.write(self.request.get('carletonID'))
        # Lookup carletonID -> get/generate verification code
        carletonAccount = models.get_user_by_CID(self.request.get('carletonID'))
        carletonAccount.verificationCode = models.generateVerificationCode()
        carletonAccount.put()
        # mail some stuff
        mailfunction.sendInvite(carletonAccount)  # tested- set to send all emails to conrad right now.
        '''http://code.google.com/appengine/docs/python/mail/sendingmail.html'''
        self.response.out.write("<br>Your pair code has been sent!!")

class Preferences(webapp.RequestHandler):
    def get(self):

        carl2carl = Carl2Carl.all()
        carl2carl.filter("source =", models.getCarl().carletonID)
        results = carl2carl.fetch(20)
        used_spots = carl2carl.count()

        #results = [pair.target for pair in results]
        results = ['a','b','c']
        total_spots = 10 # this is the number of people someone can select
        slots = ['' for i in range(total_spots)]
        carls2carls = results + slots[:len(results)]

        template_values = {
            'carls2carls': carls2carls,
            }

        path = os.path.join(os.path.dirname(__file__), 'templates/preferences.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):

        carl2carl = Carl2Carl.all()
        carl2carl.filter("source =", models.getCarl().carletonID)
        results = carl2carl.fetch(20)
        used_spots = carl2carl.count()

        total_spots = 10 # total number of people someone can select
        remaining_spots = total_spots - used_spots
        if remaining_spots < 1: remaining_spots = 0

        preferences = [self.request.get("new_carl" + str(i)) for i in range(remaining_spots) if self.request.get("new_carl" + str(i)) != ""]

        # NEED TO DEAL WITH DELETING PEOPLE!!
        ## Ohh shit that's right!

        for preference in preferences:
            if (models.get_user_by_CID(preference)):
                carl2carl = Carl2Carl()
                carl2carl.source = models.getCarl().carletonID
                carl2carl.target = preference
                carl2carl.put()
                self.response.out.write(preference + "<br>")
            else:
                self.response.out.write("cound not add " + preference + "<br>")

        self.response.out.write('<a href="/preferences">back to preferences</a>')
        
application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/preferences', Preferences),
                                      ('/pair', Pair),
                                      ('/sendPairCode', PairCode)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

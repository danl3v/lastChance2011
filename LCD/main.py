import cgi
import os

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models 
import session

import mailfunction

class MainPage(webapp.RequestHandler):
    def get(self):

        user = session.get_current_user()
        if user:
            login_url = session.create_logout_url(self.request.uri)
            login_url_linktext = 'Logout'
            
            if models.isPaired():
                pair_url = "pair"
                pair_url_linktext = "Unpair Your Account"
            else:
                pair_url = "pair"
                pair_url_linktext = "You need to pair your account"
        else:
            login_url = session.create_login_url(self.request.uri)
            login_url_linktext = 'Login'
            pair_url = ""
            pair_url_linktext = ""

  
        if session.is_current_user_admin():
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
                theCarl.googleID = str(session.get_current_user().user_id())
                theCarl.verificationCode = "" # yeah, what do we want to do with this field? should we keep the verification code there?
                theCarl.put()
                self.response.out.write("Your account was successfully paired:<br>")
                self.response.out.write("Carleton ID :" + theCarl.carletonID + "<br>")
                self.response.out.write("GoogleID: " + theCarl.googleID)
            else:
                self.response.out.write("You entered an incorrect verification code")
                self.response.out.write("Carleton ID:" + theCarl.carletonID)
                self.response.out.write("Google ID: " + str(session.get_current_user().user_id()))
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
    total_spots = 10  # this is the number of people someone can select

    def get(self):
        user = models.getCarl().carletonID  # this is its own line only because it's sort of a session-based/model operation
        user = "PAIR YOUR ACCOUNT" if user is None else user
        results = models.getCarlPreferences(user)

        results = [pair.target for pair in results]
        #results = ['a','b','c']  # temp because i just wanted to see how it'd look right now
        slots = ['' for i in range(Preferences.total_spots)]
        carls2carls = results + slots[len(results):]  # has empty trailing slots

        template_values = {
            'user': user,
            'carls2carls': carls2carls,
            }

        path = os.path.join(os.path.dirname(__file__), 'templates/preferences.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):  # Haven't figured out what to do with this yet
        user = models.getCarl().carletonID  # this is its own line only because it's sort of a session-based/model operation
        results = models.getCarlPreferences(user)  # retrieve existing preferences
        ''' Check user input for mistakes, if there are any back out.  If not, delete all previous
        entries and load new preferences into the database'''

        '''assume it's perfect for now'''
        for edge in results:
            edge.delete()

        preferences = [self.request.get("carl" + str(i)) for i in range(1,Preferences.total_spots+1)]
        for choice in preferences:
            if choice == "":
                continue
            edge = models.Carl2Carl()
            edge.source = user
            edge.target = choice
            edge.put()
            self.response.out.write("<p>"+choice + " added to your list.</p>")

        self.response.out.write('<a href="/preferences">back to preferences</a>')

        #preferences = [self.request.get("new_carl" + str(i)) for i in range(remaining_spots) if self.request.get("new_carl" + str(i)) != ""]

        # NEED TO DEAL WITH DELETING PEOPLE!!
        ## Ohh shit that's right!

"""
        for preference in preferences:
            if (models.get_user_by_CID(preference)):
                carl2carl = Carl2Carl()
                carl2carl.source = models.getCarl().carletonID
                carl2carl.target = preference
                carl2carl.put()
                self.response.out.write(preference + "<br>")
            else:
                self.response.out.write("cound not add " + preference + "<br>")

"""
        
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

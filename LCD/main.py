import cgi
import os

#from google.appengine.ext.webapp import template
#from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models 
import view
import session

import mailfunction

class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        view.renderTemplate(self, 'index.html', template_values)
        
class Pair(webapp.RequestHandler):
    def get(self):
        template_values = {}
        view.renderTemplate(self, 'pair.html', template_values)

    def post(self):
        if session.isPaired(): # unpair their account
            theCarl = session.getCarl()
            if theCarl.carletonID == self.request.get('carletonID'):
                theCarl.googleID = ""
                theCarl.put()
                self.response.out.write("Your account was successfully unpaired:<br>The following accounts are no longer associated:<br>")
                self.response.out.write("Carleton ID: " + theCarl.carletonID + "<br>")
                self.response.out.write("GoogleID: " + str(session.get_current_user().user_id()))
            else:
                self.response.out.write("Your account is not paired with " + self.request.get('carletonID') + "<br>")
                self.response.out.write("Your account is paired with:<br>")
                self.response.out.write("Carleton ID: " + theCarl.carletonID + "<br>")
                self.response.out.write("Google ID: " + str(session.get_current_user().user_id()))

        else: # pair their account
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
                self.response.out.write("Carleton ID: " + theCarl.carletonID + "<br>")
                self.response.out.write("Google ID: " + str(session.get_current_user().user_id()) + "<br>")
                self.response.out.write("Verification Code: " + theCarl.verificationCode)

class PairCode(webapp.RequestHandler):
    def post(self):
        self.response.out.write(self.request.get('carletonID'))
        # Lookup carletonID -> get/generate verification code
        carletonAccount = models.get_user_by_CID(self.request.get('carletonID'))
        carletonAccount.verificationCode = models.generateVerificationCode()
        carletonAccount.put()

        mailfunction.sendInvite(carletonAccount)  # tested- set to send all emails to conrad right now.
        '''http://code.google.com/appengine/docs/python/mail/sendingmail.html'''
        self.response.out.write("<br>Your pair code has been sent!!")

class Preferences(webapp.RequestHandler):
    total_spots = 10  # this is the number of people someone can select -- is this ok? should it go in an __init__ or something?

    def get(self):
        if session.isPaired():
            student = session.getCarl().carletonID  # this is its own line only because it's sort of a session-based/model operation
            results = models.getCarlPreferences(student)

            results = [pair.target for pair in results]
            slots = ['' for i in range(Preferences.total_spots)]
            carls2carls = results + slots[len(results):]  # has empty trailing slots

            template_values = { 'carls2carls': carls2carls }
            view.renderTemplate(self, 'preferences.html', template_values)
        else:
            self.response.out.write("You need to pair your account before entering preferences")

    def post(self):
        student = session.getCarl().carletonID  # this is its own line only because it's sort of a session-based/model operation
        results = models.getCarlPreferences(student)  # retrieve existing preferences
        
        for edge in results:
            edge.delete()
        
        preferences = [self.request.get("carl" + str(i)) for i in range(1,Preferences.total_spots+1) if self.request.get("carl" + str(i)) != ""] # maybe convert this to 0 based in the future?
        for preference in preferences:
            if models.get_user_by_CID(preference):
                edge = models.Carl2Carl()
                edge.source = student
                edge.target = preference
                edge.put()
                self.response.out.write("<p>" + preference + " added to your list.</p>")
            else:
                self.response.out.write("<p>" + preference + " could not be added.</p>")

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

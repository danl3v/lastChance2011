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
        
class OptOut(webapp.RequestHandler):
    def get(self):
        pass
    def post(self):
        pass

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
                template_values = {
                    'carletonID': theCarl.carletonID,
                    'googleID': session.get_current_user().nickname()
                    }
                view.renderTemplate(self, 'unpair_success.html', template_values)
            else:
                template_values = {
                    'carletonID_Requested': self.request.get('carletonID'),
                    'carletonID_Actual': theCarl.carletonID,
                    'googleID': session.get_current_user().nickname()
                    }
                view.renderTemplate(self, 'unpair_failure.html', template_values)
        else: # pair their account
            theCarl = models.get_user_by_CID(self.request.get('carletonID'))
            if (theCarl) and (theCarl.verificationCode == self.request.get('verificationCode')):
                theCarl.googleID = str(session.get_current_user().user_id())
                theCarl.verificationCode = "" # yeah, what do we want to do with this field? should we keep the verification code there?
                theCarl.put()
                template_values = {
                    'carletonID': theCarl.carletonID,
                    'googleID': session.get_current_user().nickname()
                    }                
                view.renderTemplate(self, 'pair_success.html', template_values)
            else:
                template_values = {
                    'pairCode' : self.request.get('verificationCode'),
                    'carletonID' : self.request.get('carletonID'),
                    'googleID' : session.get_current_user().nickname()
                    }
                view.renderTemplate(self, 'pair_failure.html', template_values)

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
                                      ('/optout', OptOut),
                                      ('/preferences', Preferences),
                                      ('/pair', Pair),
                                      ('/sendPairCode', PairCode)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

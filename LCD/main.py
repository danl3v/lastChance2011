import cgi, os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models, view, session, mailfunction

class OptOut(webapp.RequestHandler): # need to let people opt back in if they choose
    def get(self):
        theCarl = session.getCarl()

        if session.is_active(): # show optout page
            template_values = {}
            view.renderTemplate(self, 'optout.html', template_values)

        else: # show optin page
            template_values = {}
            view.renderTemplate(self, 'optin.html', template_values)

    def post(self):
        theCarl = session.getCarl()

        if session.is_active(): # make not active
            theCarl.active = False
            theCarl.put()
            template_values = {}
            view.renderTemplate(self, 'optout_success.html', template_values)

        else: # make active again
            theCarl.active = True
            theCarl.put()
            template_values = {}
            view.renderTemplate(self, 'optin_success.html', template_values)

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
                    'googleEmail': session.get_current_user().email()
                    }
                view.renderTemplate(self, 'unpair_success.html', template_values)
            else:
                template_values = {
                    'carletonID_Requested': self.request.get('carletonID'),
                    'carletonID_Actual': theCarl.carletonID,
                    'googleEmail': session.get_current_user().email()
                    }
                view.renderTemplate(self, 'unpair_failure.html', template_values)
        else: # pair their account
            theCarl = models.get_user_by_CID(self.request.get('carletonID'))
            if (theCarl) and (theCarl.verificationCode == self.request.get('verificationCode')):
                theCarl.googleID = str(session.get_current_user().user_id())
                # should we delete the verification code or leave it? we are leaving it for now so that once you unpair, you can pair again with the same code.
                # maybe if you unpair, you get an email with a new code in case you want to pair again.
                theCarl.put()
                template_values = {
                    'carletonID': theCarl.carletonID,
                    'googleEmail': session.get_current_user().email()
                    }                
                view.renderTemplate(self, 'pair_success.html', template_values)
            else:
                template_values = {
                    'pairCode' : self.request.get('verificationCode'),
                    'carletonID' : self.request.get('carletonID'),
                    'googleEmail' : session.get_current_user().email()
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
            self.response.out.write('You need to <a href="pair">pair your account</a> before entering preferences.')

    def post(self):

        carletonID = session.getCarl().carletonID
        old_preferences = models.getCarlPreferences(carletonID)  # retrieve existing preferences
        
        old_preference_ids = [old_preference.target for old_preference in old_preferences]
        new_preference_ids = [self.request.get("carl" + str(i)) for i in range(Preferences.total_spots) if self.request.get("carl" + str(i)) != ""]

        addedList = []
        removedList = []
        failedList = []

        for new_preference_id in new_preference_ids: # add new preferences
            if models.get_user_by_CID(new_preference_id):
                if new_preference_id not in old_preference_ids and new_preference_id not in addedList:
                    edge = models.Carl2Carl()
                    edge.source = carletonID
                    edge.target = new_preference_id
                    edge.put()
                    #mailfunction.sendPersonChosen(edge.target) # tested, turned off for now
                    addedList.append(new_preference_id)
            else:
                    failedList.append(new_preference_id)

        for old_preference in old_preferences: # delete the leftovers
                if old_preference.target not in new_preference_ids:
                    old_preference.delete()
                    removedList.append(old_preference.target)

        template_values = {
            'no_updates': False if addedList or removedList or failedList else True,
            'added': addedList,
            'removed': removedList,
            'failed': failedList
            }
        view.renderTemplate(self, 'preferences_success.html', template_values)

application = webapp.WSGIApplication(
                                     [('/optout', OptOut),
                                      ('/preferences', Preferences),
                                      ('/pair', Pair),
                                      ('/sendPairCode', PairCode)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
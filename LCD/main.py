import cgi, os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models, view, session, emailfunctions

class Settings(webapp.RequestHandler):

    def get(self, action=None):

        if session.is_active(): optedout = False
        else: optedout = True

        template_values = {
            'optedout': optedout
            }

        view.renderTemplate(self, 'settings.html', template_values)

    def post(self, action=None):

        if action == "optin" and not session.is_active() and session.isPaired():
            theCarl = session.getCarl()
            theCarl.active = True
            theCarl.put()
            template_values = {}
            view.renderTemplate(self, 'optin_success.html', template_values)
            
        elif action == "optout" and session.is_active() and session.isPaired():
            theCarl = session.getCarl()
            theCarl.active = False
            theCarl.put()
            template_values = {}
            view.renderTemplate(self, 'optout_success.html', template_values)

        elif action == "pair" and not session.isPaired():
            theCarl = models.get_user_by_CID(self.request.get('carletonID').split("@")[0]) # check to see if the carl is already paird with another google account
            if (theCarl) and (theCarl.verificationCode == self.request.get('verificationCode')):
                theCarl.googleID = str(session.get_current_user().user_id())
                theCarl.put()
                template_values = {
                    'carletonID': theCarl.carletonID,
                    'googleEmail': session.get_current_user().email()
                    }                
                view.renderTemplate(self, 'pair_success.html', template_values)
            else:
                template_values = {
                    'pairCode' : self.request.get('verificationCode'),
                    'carletonID' : self.request.get('carletonID').split("@")[0],
                    'googleEmail' : session.get_current_user().email()
                    }
                view.renderTemplate(self, 'pair_failure.html', template_values)

        elif action == "unpair" and session.isPaired(): # remove the need to supply a carleton id?
            theCarl = session.getCarl()
            if theCarl.carletonID == self.request.get('carletonID').split("@")[0]:
                theCarl.googleID = ""
                theCarl.put()
                template_values = {
                    'carletonID': theCarl.carletonID,
                    'googleEmail': session.get_current_user().email()
                    }
                view.renderTemplate(self, 'unpair_success.html', template_values)
            else:
                template_values = {
                    'carletonID_Requested': self.request.get('carletonID').split("@")[0],
                    'carletonID_Actual': theCarl.carletonID,
                    'googleEmail': session.get_current_user().email()
                    }
                view.renderTemplate(self, 'unpair_failure.html', template_values)

        elif action == "sendcode":
            carletonAccount = models.get_user_by_CID(self.request.get('carletonID').split("@")[0])
            carletonAccount.verificationCode = models.generateVerificationCode()
            carletonAccount.put()
            emailfunctions.sendInvite(carletonAccount)
            self.response.out.write('A pair code has been sent to ' + self.request.get('carletonID').split("@")[0] + '@carleton.edu. Once you get the email, go to <a href="/settings">settings</a> to enter your pair code.')

        else: self.response.out.write('You are not allowed to perform this action given your current user state. Please go back to <a href="/main">main</a> and try again')

class Crushes(webapp.RequestHandler):
    total_spots = 5  # this is the number of people someone can select

    def get(self):
        if session.isPaired():
            student = session.getCarl().carletonID  # this is its own line only because it's sort of a session-based/model operation
            results = models.getCarlCrushes(student)

            results = [pair.target for pair in results]
            slots = ['' for i in range(Crushes.total_spots)]
            carls2carls = results + slots[len(results):]  # has empty trailing slots

            template_values = { 'carls2carls': carls2carls }
            view.renderTemplate(self, 'crushes.html', template_values)
        else:
            self.response.out.write('You need to <a href="/settings">pair your account</a> before entering crushes.')

    def post(self):

        carletonID = session.getCarl().carletonID
        old_preferences = models.getCarlCrushes(carletonID)  # retrieve existing crushes ** rename variables to crushes
        
        old_preference_ids = [old_preference.target for old_preference in old_preferences]
        new_preference_ids = [self.request.get("carl" + str(i)) for i in range(Crushes.total_spots) if self.request.get("carl" + str(i)) != ""]

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
                    #emailfunctions.sendPersonChosen(edge.target) # tested, turned off for now
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
                                     [('/crushes', Crushes),
                                      ('/settings', Settings),
                                      ('/settings/(.*)', Settings)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

import cgi, os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import models, view, session, emailfunctions, re

class Settings(webapp.RequestHandler):

    def get(self, action=None):

        if session.is_active(): optedout = False
        else: optedout = True

        if session.isPaired(): carletonID = session.getCarl().carletonID
        else: carletonID = None

        template_values = {
            'optedout': optedout,
            'carletonID': carletonID,
            'current_page': {'settings': True}
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
            theCarl.googleID = ""
            theCarl.put()
            template_values = {
                'carletonID': theCarl.carletonID,
                'googleEmail': session.get_current_user().email()
                }
            view.renderTemplate(self, 'unpair_success.html', template_values)
            # delete unpair_failure.html

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
            carleton_id = session.getCarl().carletonID  # this is its own line only because it's sort of a session-based/model operation

            # get the crushes
            results = models.getCarlCrushes(carleton_id)
            results = [pair.target for pair in results]
            slots = ['' for i in range(Crushes.total_spots)]
            carls2carls = results + slots[len(results):]  # has empty trailing slots

            # get the messages
            messages = models.get_messages_by_CID(carleton_id)

            template_values = {
                'carls2carls': carls2carls,
                'messages': messages,
                'current_page': {'crushes': True}
                }
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

def hasCrush(source, target):
    carl2carl = models.Carl2Carl.all()
    carl2carl.filter("source =", source)
    carl2carl.filter("target =", target)
    carl = carl2carl.get()
    return carl

class AddCrush(webapp.RequestHandler):
    def post(self):
        carleton_id = session.getCarl().carletonID
        if hasCrush(carleton_id, self.request.get("crush")): self.redirect('/crushes') # alert that the crush already exists
        elif not models.get_user_by_CID(self.request.get("crush")): self.redirect('/crushes') # alert that crush does not exist
        else:
            edge = models.Carl2Carl()
            edge.source = carleton_id
            edge.target = self.request.get('crush')
            edge.put()
            self.redirect('/crushes') # add a flash that says who was added

class RemoveCrush(webapp.RequestHandler):
    def post(self):
        carleton_id = session.getCarl().carletonID
        carl = hasCrush(carleton_id, self.request.get("crush"))
        carl.delete()
        self.redirect('/crushes') # add a flash that says who was deleted

class AutoFill(webapp.RequestHandler):
    def get(self):
        terms = self.request.get("term").lower().split()
        users = models.Carl.all()
        users.order("-first_name")
        results = users.fetch(1000) #if we have more that 1000 users, we need to fetch multiple times until we run out of fetches
        theJSON = ""

        for user in users: # use list comprehension here to speed things up
            send = 0
            for term in terms:
                if (term in user.carletonID.lower()) or (term in user.first_name.lower()) or (term in user.last_name.lower()):
                    send += 1
            if send == len(terms):
                theJSON += '{"value":"' + user.first_name + ' ' + user.last_name + ' (' + user.carletonID + ')","uid":"' + user.carletonID + '"},'

        theJSON = "[" + theJSON[:-1] + "]"
        self.response.out.write(theJSON)

application = webapp.WSGIApplication(
                                     [('/crushes/add', AddCrush),
                                      ('/crushes/remove', RemoveCrush),
                                      ('/crushes', Crushes),
                                      ('/settings', Settings),
                                      ('/autofill', AutoFill),
                                      ('/settings/(.*)', Settings)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

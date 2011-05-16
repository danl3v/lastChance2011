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
            self.redirect("/settings")
            
        elif action == "optout" and session.is_active() and session.isPaired():
            theCarl = session.getCarl()
            theCarl.active = False
            theCarl.put()
            template_values = {}
            self.redirect("/settings")

        elif action == "pair" and not session.isPaired():
            theCarl = models.get_user_by_CID(self.request.get('carletonID').split("@")[0])
            if (theCarl) and (theCarl.verificationCode == self.request.get('verificationCode')):
                theCarl.googleID = str(session.get_current_user().user_id())
                theCarl.verificationCode = models.generateVerificationCode()
                theCarl.put()
                emailfunctions.send_paired(theCarl.carletonID, session.get_current_user().email())
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

        elif action == "unpair" and session.isPaired():
            theCarl = session.getCarl()
            theCarl.verificationCode = models.generateVerificationCode()
            theCarl.googleID = ""
            theCarl.put()
            emailfunctions.send_unpaired(theCarl.carletonID, session.get_current_user().email())
            template_values = {
                'carletonID': theCarl.carletonID,
                'googleEmail': session.get_current_user().email()
                }
            view.renderTemplate(self, 'unpair_success.html', template_values)

        elif action == "sendcode":
            carletonAccount = models.get_user_by_CID(self.request.get('carletonID').split("@")[0])
            if carletonAccount:
                carletonAccount.verificationCode = models.generateVerificationCode()
                carletonAccount.put()
                emailfunctions.sendInvite(carletonAccount)
                self.response.out.write('A pair code has been sent to ' + self.request.get('carletonID').split("@")[0] + '@carleton.edu. Once you get the email, go to <a href="/settings">settings</a> to enter your pair code.')
            else:
                self.response.out.write('<p>Our database does not have the user ' + self.request.get('carletonID').split("@")[0] + '. This is either beacuse you are not a senior or because you are not on stalkernet.</p>')
                self.response.out.write('<p>If you think this is our fault, <a href="/contact">contact us</a> and convince us that you are a senior.</p>')

        else: self.response.out.write('You are not allowed to perform this action. Please go back to <a href="/settings">settings</a> and try again.')

class AutoPair(webapp.RequestHandler):
    def get(self, user="", pair_code=""):
        if not session.isPaired():
            theCarl = models.get_user_by_CID(user)
            if (theCarl) and (theCarl.verificationCode == pair_code):
                theCarl.googleID = str(session.get_current_user().user_id())
                theCarl.verificationCode = models.generateVerificationCode()
                theCarl.put()
                emailfunctions.send_paired(theCarl.carletonID, session.get_current_user().email())
                template_values = {
                    'carletonID': theCarl.carletonID,
                    'googleEmail': session.get_current_user().email()
                    }                
                view.renderTemplate(self, 'pair_success.html', template_values)
            else:
                template_values = {
                    'pairCode' : pair_code,
                    'carletonID' : user,
                    'googleEmail' : session.get_current_user().email()
                    }
                view.renderTemplate(self, 'pair_failure.html', template_values)
        else:
            self.response.out.write('Your Google ID is already paired to another Carleton ID')
            
class Crushes(webapp.RequestHandler):
    def get(self):
        if session.isPaired() and session.is_active():
            carleton_id = session.getCarl().carletonID
            crushes = models.getCarlCrushes(carleton_id)
            messages = models.get_messages_by_CID(carleton_id)
            template_values = {
                'crushes': crushes,
                'messages': messages,
                'current_page': { 'crushes': True }
                }
            view.renderTemplate(self, 'crushes.html', template_values)
        else:
            self.response.out.write('Your account must be paired and opted-in before adding crushes. Go to <a href="/settings">settings</a> to resolve this issue.')

class AddCrush(webapp.RequestHandler):
    def post(self):
        if session.isPaired() and session.is_active():
            carleton_id = session.getCarl().carletonID # can optimize this a bit since hasCrush returns the target user if the crush exists
            if models.hasCrush(carleton_id, self.request.get("crush")): self.response.out.write('{"success":2}') # cannot choose someone who is already a crush
            elif not models.get_user_by_CID(self.request.get("crush")): self.response.out.write('{"success":3}') # crush must exist
            elif not models.get_user_by_CID(self.request.get("crush")).active: self.response.out.write('{"success":4}') # crush must not be opted out
            elif carleton_id == self.request.get("crush"): self.response.out.write('{"success":5}') # can't choose yourself as a crush
            else:
                edge = models.Carl2Carl()
                edge.source = carleton_id
                edge.target = self.request.get('crush')
                edge.put()
                self.response.out.write('{"success":0}')
        else:
            self.response.out.write('{"success":1}')    

class RemoveCrush(webapp.RequestHandler):
    def post(self):
        if session.isPaired() and session.is_active():
            carleton_id = session.getCarl().carletonID
            carl = models.hasCrush(carleton_id, self.request.get("crush"))
            carl.delete()
            self.response.out.write('{"success":0}')
        else:
            self.response.out.write('{"success":1}')

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
                if (term in user.carletonID.lower()) or (term in user.first_name.lower()) or (term in user.last_name.lower()): send += 1
            if send == len(terms):
                theJSON += '{"value":"' + user.first_name + ' ' + user.last_name + ' (' + user.carletonID + ')","carletonID":"' + user.carletonID + '","first_name":"' + user.first_name + '","last_name":"' + user.last_name + '"},'

        theJSON = "[" + theJSON[:-1] + "]"
        self.response.out.write(theJSON)

application = webapp.WSGIApplication(
                                     [('/crushes/add', AddCrush),
                                      ('/crushes/remove', RemoveCrush),
                                      ('/crushes', Crushes),
                                      ('/settings', Settings),
                                      ('/pair/(.*)/(.*)', AutoPair),
                                      ('/autofill', AutoFill),
                                      ('/settings/(.*)', Settings)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

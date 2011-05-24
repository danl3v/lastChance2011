from google.appengine.ext import webapp
from models import models
import session, view, emailfunctions, functions

class Settings(webapp.RequestHandler):

    def get(self, action=None):

        if session.opted_in(): optedout = False
        else: optedout = True

        if session.isPaired(): carletonID = session.getCarl().carletonID
        else: carletonID = None

        template_values = {
            'carletonID': carletonID,
            'current_page': { 'settings': True }
            }

        view.renderTemplate(self, 'settings.html', template_values)

    def post(self, action=None):

        if action == "optin" and not session.opted_in() and session.isPaired():
            theCarl = session.getCarl()
            theCarl.opted_in = True
            theCarl.put()

            ''' #tested
            crushes = get_crushes_for_user_by_target(theCarl) # send opted in notifications
            for crush in crushes:
                if crush.source.opted_in: emailfunctions.send_opted_in(crush.source, crush.target)
            '''

            self.redirect("/settings")
            
        elif action == "optout" and session.opted_in() and session.isPaired():
            theCarl = session.getCarl()
            theCarl.opted_in = False
            theCarl.put()

            ''' #tested
            crushes = get_crushes_for_user_by_target(theCarl) # send opted out notifications
            for crush in crushes:
                if crush.source.opted_in: emailfunctions.send_opted_out(crush.source, crush.target)
            '''
                
            self.redirect("/settings")

        elif action == "pair" and not session.isPaired():
            theCarl = functions.get_user_by_CID(self.request.get('carletonID').split("@")[0])
            if (theCarl) and (theCarl.pair_code == self.request.get('pair_code')):
                theCarl.googleID = str(session.get_current_user().user_id())
                theCarl.pair_code = functions.generate_pair_code()
                theCarl.put()
                #emailfunctions.send_paired(theCarl, session.get_current_user())
                template_values = {
                    'carletonID': theCarl.carletonID,
                    'googleEmail': session.get_current_user().email()
                    }
                view.renderTemplate(self, 'pair_success.html', template_values)
            else:
                template_values = {
                    'pairCode' : self.request.get('pair_code'),
                    'carletonID' : self.request.get('carletonID').split("@")[0],
                    'googleEmail' : session.get_current_user().email()
                    }
                view.renderTemplate(self, 'pair_failure.html', template_values)

        elif action == "unpair" and session.isPaired():
            theCarl = session.getCarl()
            theCarl.pair_code = functions.generate_pair_code()
            theCarl.googleID = None
            theCarl.put()
            #emailfunctions.send_unpaired(theCarl, session.get_current_user())
            template_values = {
                'carletonID': theCarl.carletonID,
                'googleEmail': session.get_current_user().email()
                }
            view.renderTemplate(self, 'unpair_success.html', template_values)

        elif action == "invite":
            carletonAccount = functions.get_user_by_CID(self.request.get('carletonID').split("@")[0])
            if carletonAccount:
                carletonAccount.pair_code = functions.generate_pair_code()
                carletonAccount.put()
                emailfunctions.send_invitation(carletonAccount)
                self.response.out.write('{"success":0}')
            else:
                self.response.out.write('{"success":1}')

class AutoPair(webapp.RequestHandler):
    def get(self, user="", pair_code=""):
        theCarl = functions.get_user_by_CID(user)
        if (theCarl) and (theCarl.pair_code == pair_code):
            theCarl.googleID = str(session.get_current_user().user_id())
            theCarl.pair_code = functions.generate_pair_code()
            theCarl.put()
            #emailfunctions.send_paired(theCarl, session.get_current_user())
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

def get_crushes_for_user_by_target(user):
    crushes = models.Crush.all()
    crushes.filter("target =", user)
    return crushes.fetch(1000) # there should not be more than num users in db

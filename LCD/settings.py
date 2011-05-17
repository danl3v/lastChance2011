from google.appengine.ext import webapp
import session, models, view, emailfunctions, functions

class Settings(webapp.RequestHandler):

    def get(self, action=None):

        if session.is_active(): optedout = False
        else: optedout = True

        if session.isPaired(): carletonID = session.getCarl().carletonID
        else: carletonID = None

        template_values = {
            'optedout': optedout, # active is always passed in, should resolve this issue
            'carletonID': carletonID,
            'current_page': { 'settings': True }
            }

        view.renderTemplate(self, 'settings.html', template_values)

    def post(self, action=None):

        if action == "optin" and not session.is_active() and session.isPaired():
            theCarl = session.getCarl()
            theCarl.active = True
            theCarl.put()

            ''' #tested
            sources = get_crushes_for_user_by_target(theCarl.carletonID) # send opted in notifications
            for source in sources:
                emailfunctions.send_opted_in(source, theCarl)
            '''

            self.redirect("/settings")
            
        elif action == "optout" and session.is_active() and session.isPaired():
            theCarl = session.getCarl()
            theCarl.active = False
            theCarl.put()

            ''' #tested
            sources = get_crushes_for_user_by_target(theCarl.carletonID) # send opted out notifications
            for source in sources:
                emailfunctions.send_opted_out(source, theCarl)
            '''
                
            self.redirect("/settings")

        elif action == "pair" and not session.isPaired():
            theCarl = functions.get_user_by_CID(self.request.get('carletonID').split("@")[0])
            if (theCarl) and (theCarl.verificationCode == self.request.get('verificationCode')):
                theCarl.googleID = str(session.get_current_user().user_id())
                theCarl.verificationCode = functions.generate_pair_code()
                theCarl.put()
                emailfunctions.send_paired(theCarl, session.get_current_user())
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
            theCarl.verificationCode = functions.generate_pair_code()
            theCarl.googleID = ""
            theCarl.put()
            emailfunctions.send_unpaired(theCarl, session.get_current_user())
            template_values = {
                'carletonID': theCarl.carletonID,
                'googleEmail': session.get_current_user().email()
                }
            view.renderTemplate(self, 'unpair_success.html', template_values)

        elif action == "sendcode":
            carletonAccount = functions.get_user_by_CID(self.request.get('carletonID').split("@")[0])
            if carletonAccount:
                carletonAccount.verificationCode = functions.generate_pair_code()
                carletonAccount.put()
                emailfunctions.send_invitation(carletonAccount)
                self.response.out.write('A pair code has been sent to ' + self.request.get('carletonID').split("@")[0] + '@carleton.edu. Once you get the email, go to <a href="/settings">settings</a> to enter your pair code.')
            else:
                self.response.out.write('<p>Our database does not have the user ' + self.request.get('carletonID').split("@")[0] + '. This is either beacuse you are not a senior or because you are not on stalkernet.</p>')
                self.response.out.write('<p>If you think this is our fault, <a href="/contact">contact us</a> and convince us that you are a senior.</p>')

        else: self.response.out.write('You are not allowed to perform this action. Please go back to <a href="/settings">settings</a> and try again.')

class AutoPair(webapp.RequestHandler):
    def get(self, user="", pair_code=""):
        theCarl = functions.get_user_by_CID(user)
        if (theCarl) and (theCarl.verificationCode == pair_code):
            theCarl.googleID = str(session.get_current_user().user_id())
            theCarl.verificationCode = functions.generate_pair_code()
            theCarl.put()
            emailfunctions.send_paired(theCarl, session.get_current_user())
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
    carl2carl = models.Carl2Carl.all()
    carl2carl.filter("target =", user)
    results = carl2carl.fetch(1000) # there should not be more than num users in db
    return [functions.get_user_by_CID(result.source) for result in results]

from google.appengine.ext import webapp
from google.appengine.ext import db
from models import models
import view, session, emailfunctions, functions

def addCarl(first_name, last_name, carleton_id):
    if functions.get_user_by_CID(carleton_id.strip()):
        return False
    else:
        carl = models.Carl()
        carl.carletonID = carleton_id.strip()
        carl.pair_code = functions.generate_pair_code()
        carl.first_name = first_name.strip()
        carl.last_name = last_name.strip()
        carl.put()
        return True

class CalculateMatches(webapp.RequestHandler):
    def get(self):
        matches = functions.update_matches()

class SendMatchNotifications(webapp.RequestHandler):
    def get(self):
        users = models.Carl.all()
        # get the matches and send out notifications


class Admin(webapp.RequestHandler):
    def get(self):
        carls = models.Carl.all()
        template_values = {
            'carls' : carls,
            'current_page': { 'admin': True }
        }
        view.renderTemplate(self, 'admin.html', template_values)

class AddCarl(webapp.RequestHandler):
    def post(self):
        addCarl(self.request.get("first_name"), self.request.get("last_name"), self.request.get('carletonID'))
        self.redirect('/admin')

class AddUsers(webapp.RequestHandler):
    def post(self):
        users = self.request.get("users").split("\n")
        for user in users:
            if user == "": continue
            (first_name, last_name, carleton_id) = user.split(",")
            addCarl(first_name, last_name, carleton_id)
        self.redirect('/admin')

class DeleteCarl(webapp.RequestHandler):
    def post(self):
        carl = functions.get_user_by_CID(self.request.get('carletonID'))
        carl.delete()
        self.redirect('/admin')

class NewPairCode(webapp.RequestHandler):
    def post(self):
        carl = functions.get_user_by_CID(self.request.get('carletonID'))
        carl.pair_code = functions.generate_pair_code()
        carl.put()
        self.redirect('/admin')

class UnPairCarl(webapp.RequestHandler):
    def post(self):
        carl = functions.get_user_by_CID(self.request.get('carletonID'))
        carl.googleID = ""
        carl.put()
        self.redirect('/admin')

class Invite(webapp.RequestHandler):
    def post(self):
        carletonAccount = functions.get_user_by_CID(self.request.get("carletonID"))
        emailfunctions.send_invitation(carletonAccount)
        self.response.out.write('Invitation sent to ' + self.request.get("carletonID") + '! <a href="/admin">Back to admin</a>.')

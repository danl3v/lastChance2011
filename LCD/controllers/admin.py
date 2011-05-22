from google.appengine.ext import webapp
from models import models
import view, session, emailfunctions, functions

class Admin(webapp.RequestHandler):
    def get(self):
        carls = models.Carl.all()
        
        template_values = {
            'carls' : carls,
            'site_status': functions.get_site_status(),
            'current_page': { 'admin': True }
        }
        view.renderTemplate(self, 'admin.html', template_values)

class SetSiteStatus(webapp.RequestHandler):
    def post(self):
        new_site_status = self.request.get("site_status")
        if new_site_status not in ["pre", "open", "calculating", "showing"]:
            self.response.out.write('{"success":1, "status":"' + new_site_status + '"}')
        else:
            site_status = models.Setting.all().filter("name =", "site_status").get()
            if not site_status:
                site_status = models.Setting()
                site_status.name = "site_status"
                site_status.value = new_site_status
                site_status.put()
            else:
                site_status.value = new_site_status
                site_status.put()
            self.response.out.write('{"success":0, "status":"' + new_site_status + '"}')

class UpdateMatches(webapp.RequestHandler):
    def get(self):
        matches = functions.update_matches()
        self.response.out.write('{"success":0}')

class SendMatchNotifications(webapp.RequestHandler):
    def get(self):
        users = models.Carl.all()
        for user in users:
            matches = user.matches.fetch(10)
            if len(matches) > 0:
                emailfunctions.send_matches(user, matches)
        self.response.out.write('{"success":0}')

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

class InviteAll(webapp.RequestHandler):
    def get(self):
        users = models.Carl.all()
        for user in users:
            emailfunctions.send_invitation(user)
        self.response.out.write('{"success":0}')

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

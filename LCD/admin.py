import cgi
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models, view, session, emailfunctions, functions

def addCarl(first_name, last_name, carleton_id):
    if functions.get_user_by_CID(carleton_id.strip()):
        return False
    else:
        carl = models.Carl()
        carl.carletonID = carleton_id.strip()
        carl.verificationCode = functions.generate_pair_code()
        carl.first_name = first_name.strip()
        carl.last_name = last_name.strip()
        carl.put()
        return True

class CalculateCrushes(webapp.RequestHandler):
    def get(self):
        matches = calculate_matches()
        for match in matches:
            self.response.out.write(match[0] + " --> " + match[1] + "<br>")
            # send emails here

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
        carl.verificationCode = functions.generate_pair_code()
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
        emailfunctions.sendInvite(carletonAccount)
        self.response.out.write('Invitation sent to ' + self.request.get("carletonID") + '! <a href="/admin">Back to admin</a>.')

def has_crush(source, target):
    carl2carl = models.Carl2Carl.all()
    carl2carl.filter("source =", source)
    carl2carl.filter("target =", target)
    carl = carl2carl.get()
    return carl

def calculate_matches():
    crushes = models.Carl2Carl.all()
    return [(crush.source, crush.target) for crush in crushes if has_crush(crush.target, crush.source)]

application = webapp.WSGIApplication(
                                      [('/admin', Admin),
                                       ('/admin/', Admin),
                                       ('/admin/addcarl', AddCarl),
                                       ('/admin/addusers', AddUsers),
                                       ('/admin/newpaircode', NewPairCode),
                                       ('/admin/deletecarl', DeleteCarl),
                                       ('/admin/invite', Invite),
                                       ('/admin/unpaircarl', UnPairCarl),
                                       ('/admin/calculate', CalculateCrushes)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

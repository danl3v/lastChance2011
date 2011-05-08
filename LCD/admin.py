import cgi
import os

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models, view, session, emailfunctions

def addCarl(first_name, last_name, carleton_id):
    if models.get_user_by_CID(carleton_id.strip()):
        return False
    else:
        carl = models.Carl()
        carl.carletonID = carleton_id.strip()
        carl.verificationCode = models.generateVerificationCode()
        carl.first_name = first_name.strip()
        carl.last_name = last_name.strip()
        carl.put()
        return True

class Admin(webapp.RequestHandler):
    def get(self):
        carls = models.Carl.all()
        template_values = {
            'carls' : carls,
            'current_page': {'admin': True}
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
        carl = models.get_user_by_CID(self.request.get('carletonID'))
        carl.delete()
        self.redirect('/admin')

class NewPairCode(webapp.RequestHandler):
    def post(self):
        carl = models.get_user_by_CID(self.request.get('carletonID'))
        carl.verificationCode = models.generateVerificationCode()
        carl.put()
        self.redirect('/admin')

class UnPairCarl(webapp.RequestHandler):
    def post(self):
        carl = models.get_user_by_CID(self.request.get('carletonID'))
        carl.googleID = ""
        carl.put()
        self.redirect('/admin')

class Invite(webapp.RequestHandler):
    def post(self):
        carletonAccount = models.get_user_by_CID(self.request.get("carletonID"))
        emailfunctions.sendInvite(carletonAccount)
        self.response.out.write('Invitation sent to ' + self.request.get("carletonID") + '! <a href="/admin">Back to admin</a>.')

application = webapp.WSGIApplication(
                                      [('/admin', Admin),
                                       ('/admin/', Admin),
                                       ('/admin/addcarl', AddCarl),
                                       ('/admin/addusers', AddUsers),
                                       ('/admin/newpaircode', NewPairCode),
                                       ('/admin/deletecarl', DeleteCarl),
                                       ('/admin/invite', Invite),
                                       ('/admin/unpaircarl', UnPairCarl)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

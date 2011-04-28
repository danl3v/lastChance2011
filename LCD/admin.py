import cgi
import os

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models
import view
import session

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
        carl = models.Carl() # NEED TO CHECK IF USER WITH THAT ID ALREADY EXISTS IN DB, or for empty user
        carl.carletonID = self.request.get('carletonID')
        carl.verificationCode = models.generateVerificationCode() # do we want to generate an authentication code here or when we send out an invite?
        carl.put()
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

application = webapp.WSGIApplication(
                                      [('/admin', Admin),
                                       ('/admin/', Admin),
                                       ('/admin/addcarl', AddCarl),
                                       ('/admin/newpaircode', NewPairCode),
                                       ('/admin/deletecarl', DeleteCarl),
                                       ('/admin/unpaircarl', UnPairCarl)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

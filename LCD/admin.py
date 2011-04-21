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
            'carls' : carls
        }
        view.renderTemplate(self, 'admin.html', template_values)

class AddCarl(webapp.RequestHandler):
    def post(self):
        carl = models.Carl() # NEED TO CHECK IF USER WITH THAT ID ALREADY EXISTS IN DB, or for empty user
        carl.carletonID = self.request.get('carletonID')
        carl.verificationCode = models.generateVerificationCode() # do we want to generate an authentication code here or when we send out an invite?
        carl.put()
        self.redirect('/admin')

'''
we should write functions to do the pairing and unpairing, and then we can call them here or on the other pages where a user pairs their account as needed.

'''

class DeleteCarl(webapp.RequestHandler):
    def post(self):
        pass

class PairCarl(webapp.RequestHandler):
    def post(self):
        pass

class UnPairCarl(webapp.RequestHandler):
    def post(self):
        pass


application = webapp.WSGIApplication(
                                      [('/admin', Admin),
                                       ('/admin/', Admin),
                                      ('/admin/addcarl', AddCarl)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

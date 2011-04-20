import cgi
import os

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models
import session

def getNavData(self):
    user = session.get_current_user()
    if user:
        login_url = session.create_logout_url(self.request.uri)
        login_url_linktext = 'Logout'
        
        if models.isPaired():
            pair_url = "pair"
            pair_url_linktext = "Unpair Your Account"
        else:
            pair_url = "pair"
            pair_url_linktext = "You need to pair your account"
    else:
        login_url = session.create_login_url(self.request.uri)
        login_url_linktext = 'Login'
        pair_url = ""
        pair_url_linktext = ""
        
    if session.is_current_user_admin():
        admin = True
    else:
        admin = False

    return {
        'user': user,
        'admin': admin,
        'login_url': login_url,
        'login_url_linktext': login_url_linktext,
        'pair_url': pair_url,
        'pair_url_linktext': pair_url_linktext
        }

def renderTemplate(self, template_file, template_values):

    template_values = dict(getNavData(self), **template_values)

    path = os.path.join(os.path.dirname(__file__), 'templates/header.html')
    self.response.out.write(template.render(path, template_values))
    
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_file)
    self.response.out.write(template.render(path, template_values))
    
    path = os.path.join(os.path.dirname(__file__), 'templates/footer.html')
    self.response.out.write(template.render(path, template_values))


class Admin(webapp.RequestHandler):
    def get(self):
        carls = models.Carl.all()
        template_values = {
            'carls' : carls
        }
        renderTemplate(self, 'admin.html', template_values)
class AddCarl(webapp.RequestHandler):
    def post(self):
        carl = models.Carl() # NEED TO CHECK IF USER WITH THAT ID ALREADY EXISTS IN DB, or for empty user
        carl.carletonID = self.request.get('carletonID')
        carl.verificationCode = generateVerificationCode() # do we want to generate an authentication code here or when we send out an invite?
        carl.put()
        self.redirect('/admin')

application = webapp.WSGIApplication(
                                      [('/admin', Admin),
                                       ('/admin/', Admin),
                                      ('/admin/addcarl', AddCarl)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

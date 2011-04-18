import cgi
import os

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Carl(db.Model):
    googleAccount = db.UserProperty()
    carletonID = db.StringProperty()

class Carl2Carl(db.Model):
    source = db.StringProperty()
    target = db.StringProperty()
    

class MainPage(webapp.RequestHandler):
    def get(self):

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class Guestbook(webapp.RequestHandler):
    def post(self):
        greeting = Greeting()

        if users.get_current_user():
            greeting.author = users.get_current_user()
        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')

class Admin(webapp.RequestHandler):
    def get(self):
        pass

class Preferences(webapp.RequestHandler):
    def get(self):

        user = users.get_current_user()
        carl = db.GqlQuery("SELECT * from Carl WHERE googleAccount=" + user.user_id())
        preferences = db.GqlQuery("SELECT * FROM Carl2Carl WHERE source='" + carl.carletonID + "'")

        template_values = {
            'user': user,
            'preferences': preferences
        }

        path = os.path.join(os.path.dirname(__file__), 'preferences.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        pass

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/admin', Admin),
                                      ('/preferences', Preferences)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

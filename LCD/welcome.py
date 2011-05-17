from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import view, session, emailfunctions

class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = { 'current_page': {'main': True} }
        view.renderTemplate(self, 'index.html', template_values)

class Contact(webapp.RequestHandler):
    def get(self):
        user = session.get_current_user()
        template_values = {
            'user': user
            }
        view.renderTemplate(self, 'contact.html', template_values)
    def post(self):
        emailfunctions.send_contact_form(self.request.get("subject"), self.request.get("body"), self.request.get("anonymous"))
        template_values = {}
        view.renderTemplate(self, 'contact_success.html', template_values)

def main():
    application = webapp.WSGIApplication([
           ('/', MainPage),
           ('/contact', Contact)
         ],debug=True)

    run_wsgi_app(application)

if __name__ == "__main__":
    main()

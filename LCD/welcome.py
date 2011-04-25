from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import view

class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        view.renderTemplate(self, 'index.html', template_values)

class Privacy(webapp.RequestHandler):
    def get(self):
        template_values = {}
        view.renderTemplate(self, 'privacy.html', template_values)

class Contact(webapp.RequestHandler):
    def get(self):
        template_values = {}
        view.renderTemplate(self, 'contact.html', template_values)


application = webapp.WSGIApplication(
                                      [('/', MainPage),
                                       ('/privacy', Privacy),
                                       ('/contact', Contact)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

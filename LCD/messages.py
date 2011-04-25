import cgi, os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models, view, session, emailfunctions

class Inbox(webapp.RequestHandler):
    def get(self):
        
        template_values = { }
        view.renderTemplate(self, 'inbox.html', template_values)
    def post(self):
        newMessage = models.Message()
        newMessage.target = self.request.get("to")
        newMessage.message = self.request.get("body")
        newMessage.put()
        template_values = { }
        view.renderTemplate(self, 'inbox.html', template_values)

application = webapp.WSGIApplication(
                                     [('/messages/', Inbox) ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

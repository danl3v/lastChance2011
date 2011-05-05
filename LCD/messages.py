import cgi, os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models, view, session, emailfunctions

class Send(webapp.RequestHandler):
    def post(self):

        if session.isPaired(): # also check to see if user exists
            newMessage = models.Message()
            newMessage.source = session.getCarl().carletonID
            newMessage.target = self.request.get("to")
            newMessage.message = self.request.get("body")
            newMessage.read = False
            newMessage.put()
            self.response.out.write('{"success":0}')
        else:
            self.response.out.write('{"success":1}')

application = webapp.WSGIApplication(
                                     [('/messages/send', Send)], debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

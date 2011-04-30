import cgi, os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models, view, session, emailfunctions

class Inbox(webapp.RequestHandler):

    def get(self):
        if session.isPaired():
            carleton_id = session.getCarl().carletonID
            messages = models.get_messages_by_CID(carleton_id)
        
            template_values = {
               'messages': messages,
               'current_page': {'messages': True}
            }
            view.renderTemplate(self, 'inbox.html', template_values)
        else:
            self.response.out.write('You need to <a href="/settings">pair your account</a> before using messages.')

class Send(webapp.RequestHandler):
    def post(self):
        if session.isPaired():
            newMessage = models.Message()
            newMessage.source = "nobody"
            newMessage.target = self.request.get("to")
            newMessage.message = self.request.get("body")
            newMessage.read = False
            newMessage.put()
            self.redirect("/messages/")
        else:
            self.response.out.write('You need to <a href="/settings">pair your account</a> before using messages.')

application = webapp.WSGIApplication(
                                     [('/messages.?', Inbox),
                                     ('/messages/send', Send) ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

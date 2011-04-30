import cgi, os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models, view, session, emailfunctions

class Inbox(webapp.RequestHandler):
    def get(self):
        import hashlib
        carl = session.getCarl().carletonID
        messages = models.get_messages_by_CID(carl)
        for m in messages:
            m.source = hashlib.sha224(m.source).hexdigest()
        
        template_values = {
           'messages': messages }
        view.renderTemplate(self, 'inbox.html', template_values)


class Send(webapp.RequestHandler):
    def post(self):
        newMessage = models.Message()
        newMessage.source = session.getCarl().carletonID
        newMessage.target = self.request.get("to")
        newMessage.message = self.request.get("body")
        newMessage.read = False
        newMessage.put()
        self.redirect("/messages/")

application = webapp.WSGIApplication(
                                     [('/messages.?', Inbox),
                                     ('/messages/send', Send) ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

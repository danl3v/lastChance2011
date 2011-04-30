import cgi, os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models, view, session, emailfunctions
import sitemessages

class Inbox(webapp.RequestHandler):
    def get(self):
        import hashlib
        carl = session.getCarl().carletonID
        messages = models.get_messages_by_CID(carl)
        # hide sender
        for m in messages:
            m.source = hashlib.md5(m.source).hexdigest()
            #m.source = hashlib.md5(m.source+m.target).hexdigest() # If we want to be really cute
            ''' maybe go one step further so hashes are readable '''
        
        template_values = {
           'messages': messages }
        view.renderTemplate(self, 'inbox.html', template_values)


class Send(webapp.RequestHandler):
    def post(self):
        target = self.request.get("to")
        message = self.request.get("body")
        sitemessages.sendMessage(target,message)
        self.redirect("/messages/")

application = webapp.WSGIApplication(
                                     [('/messages.?', Inbox),
                                     ('/messages/send', Send) ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

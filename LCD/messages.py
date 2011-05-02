import cgi, os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models, view, session, emailfunctions
#import sitemessages

class Inbox(webapp.RequestHandler):

    def get(self):
        if session.isPaired():
            carleton_id = session.getCarl().carletonID
            messages = models.get_messages_by_CID(carleton_id)

            ''' #Leaving this here till we figure out if we need it or not
            import hashlib
            carl = session.getCarl().carletonID
            messages = models.get_messages_by_CID(carl)
            # hide sender
            for m in messages:
            m.source = hashlib.md5(m.source).hexdigest()
            #m.source = hashlib.md5(m.source+m.target).hexdigest() # If we want to be really cute
            # maybe go one step further so hashes are readable 
            '''        
        
            template_values = {
               'messages': messages,
               'current_page': {'inbox': True}
            }
            view.renderTemplate(self, 'inbox.html', template_values)
        else:
            self.response.out.write('You need to <a href="/settings">pair your account</a> before using messages.')

class Send(webapp.RequestHandler):
    def post(self):

        if session.isPaired(): # also check to see if user exists
            newMessage = models.Message()
            newMessage.source = session.getCarl().carletonID
            newMessage.target = self.request.get("to")
            newMessage.message = self.request.get("body")
            newMessage.read = False
            newMessage.put()
            #self.redirect("/messages/")
            self.response.out.write("0")
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

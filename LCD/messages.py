import cgi, os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models, view, session, emailfunctions

class Send(webapp.RequestHandler):
    def post(self):
        if session.isPaired() and session.is_active():
            carleton_id = session.getCarl().carletonID
            if not models.get_user_by_CID(self.request.get("to")): self.response.out.write('{"success":2}')
            elif not models.get_user_by_CID(self.request.get("to")).active: self.response.out.write('{"success":3}')
            elif not models.hasCrush(carleton_id, self.request.get("to")): self.response.out.write('{"success":4}')
            else:
                message = models.Message()
                message.source = carleton_id
                message.target = self.request.get("to")
                message.message = self.request.get("body")
                message.read = False
                message.put()
                self.response.out.write('{"success":0}')
        else:
            self.response.out.write('{"success":1}')

application = webapp.WSGIApplication(
                                     [('/messages/send', Send)], debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
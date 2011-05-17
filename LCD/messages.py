from google.appengine.ext import webapp
import models, view, session, functions

class Send(webapp.RequestHandler):
    def post(self):
        if session.isPaired() and session.is_active():
            carleton_id = session.getCarl().carletonID
            if not functions.get_user_by_CID(self.request.get("to")): self.response.out.write('{"success":2}') # check if user exists
            elif not functions.has_crush(carleton_id, self.request.get("to")): self.response.out.write('{"success":3}') # you must have them as a crush
            else:
                message = models.Message()
                message.source = carleton_id
                message.target = self.request.get("to")
                message.message = self.request.get("body")
                message.put()
                self.response.out.write('{"success":0}')
        else:
            self.response.out.write('{"success":1}')

class Delete(webapp.RequestHandler):
    def post(self):
        if session.isPaired() and session.is_active():
            carleton_id = session.getCarl().carletonID
            message = models.Message.get_by_id(long(self.request.get("mid"))) # maybe use key instead of key.id to find the message
            if message and message.target == carleton_id: # users can only delete their own messages
                message.deleted = True
                message.put()
                self.response.out.write('{"success":0}')
            else:
                self.response.out.write('{"success":2}')
        else:
            self.response.out.write('{"success":1}')

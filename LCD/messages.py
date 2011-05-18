from google.appengine.ext import webapp
import models, view, session, functions

class Send(webapp.RequestHandler):
    def post(self):
        if session.isPaired() and session.opted_in():
            source = session.getCarl()
            target = functions.get_user_by_CID(self.request.get("to"))
            if not target: self.response.out.write('{"success":2}') # check if user exists
            elif not functions.has_crush(source, target): self.response.out.write('{"success":3}') # you must have them as a crush
            else:
                message = models.Message()
                message.source = source
                message.target = target
                message.body = self.request.get("body")
                message.put()
                self.response.out.write('{"success":0}')
        else:
            self.response.out.write('{"success":1}')

class Reply(webapp.RequestHandler):
    def post(self):
        if session.isPaired() and session.opted_in():
            message = models.Message.get_by_id(long(self.request.get("mid"))) # maybe use key instead of key.id to find the message
            source = session.getCarl()
            if message and (message.source.carletonID == source.carletonID or message.target.carletonID == source.carletonID):
                reply = models.Reply()
                reply.message = message
                reply.source = source
                reply.body = self.request.get("body")
                reply.put()
                self.response.out.write('{"success":0}')
            else:
                self.response.out.write('{"success":2}')
        else:
            self.response.out.write('{"success":1}')

class Delete(webapp.RequestHandler):
    def post(self):
        if session.isPaired() and session.opted_in():
            target = session.getCarl()
            message = models.Message.get_by_id(long(self.request.get("mid"))) # maybe use key instead of key.id to find the message
            if message and message.target.carletonID == target.carletonID: # kind of weird that we need to compare their carletonIDs instead of just comparing them
                message.deleted = True
                message.put()
                self.response.out.write('{"success":0}')
            else:
                self.response.out.write('{"success":2}')
        else:
            self.response.out.write('{"success":1}')

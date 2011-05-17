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
                thread = models.Thread()
                thread.source = source
                thread.target = target
                thread.message = self.request.get("body")
                thread.put()
                self.response.out.write('{"success":0}')
        else:
            self.response.out.write('{"success":1}')

class Delete(webapp.RequestHandler):
    def post(self):
        if session.isPaired() and session.opted_in():
            target = session.getCarl()
            thread = models.Thread.get_by_id(long(self.request.get("mid"))) # maybe use key instead of key.id to find the thread
            if thread and thread.target.carletonID == target.carletonID: # kind of weird that we need to compare their carletonIDs instead of just comparing them
                thread.deleted = True
                thread.put()
                self.response.out.write('{"success":0}')
            else:
                self.response.out.write('{"success":2}')
        else:
            self.response.out.write('{"success":1}')

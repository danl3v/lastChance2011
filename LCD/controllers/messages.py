from google.appengine.ext import webapp
from datetime import datetime
from models import models
import view, session, functions

class Send(webapp.RequestHandler):
    @functions.only_if_site_open
    @functions.only_if_paired_opted_in
    def post(self):
            source = session.getCarl()
            target = functions.get_user_by_CID(self.request.get("to"))
            if not target: self.response.out.write('{"success":2}') # check if user exists
            elif not functions.has_crush(source, target): self.response.out.write('{"success":3}') # you must have them as a crush
            elif not self.request.get("body"): self.response.out.write('{"success":4}') # message must have a body
            else:
                message = models.Message()
                message.source = source
                message.target = target
                message.body = self.request.get("body")
                message.put()

                target.num_unread_messages += 1
                target.put()

                self.response.out.write('{"success":0,"mid":' + str(message.key().id()) + ',"name":"' + message.target.first_name + ' ' + message.target.last_name + '"}')

class Reply(webapp.RequestHandler):
    @functions.only_if_site_open
    @functions.only_if_paired_opted_in
    def post(self):
        message = models.Message.get_by_id(long(self.request.get("mid"))) # maybe use key instead of key.id to find the message
        source = session.getCarl()
        if message and (message.source.carletonID == source.carletonID or message.target.carletonID == source.carletonID):

            reply = models.Reply()

            if message.source.carletonID == source.carletonID: # then we set the target as unread   
                reply.source_unread = False
                message.target.num_unread_messages += 1
                message.target.put()

            elif message.target.carletonID == source.carletonID: # then we set the source as unread
                reply.target_unread = False
                message.source.num_unread_messages += 1
                message.source.put()
                
            reply.message = message
            reply.source = source
            reply.body = self.request.get('body')
            reply.put()
            
            message.updated = datetime.now()
            message.source_deleted = False
            message.target_deleted = False
            message.put()
            
            self.response.out.write('{"success":0}')
            
        self.response.out.write('{"success":2}')

class Delete(webapp.RequestHandler):
    @functions.only_if_site_open
    @functions.only_if_paired_opted_in
    def post(self):
        user = session.getCarl()
        message = models.Message.get_by_id(long(self.request.get("mid"))) # maybe use key instead of key.id to find the message
        if message:
            if user.carletonID == message.source.carletonID: message.source_deleted = True
            elif user.carletonID == message.target.carletonID: message.target_deleted = True
            message.put()
            self.response.out.write('{"success":0}')
        else:
            self.response.out.write('{"success":2}')
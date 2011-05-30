from google.appengine.ext import webapp
from models import models
import view, session, functions, emailfunctions

class Get(webapp.RequestHandler):
    @functions.only_if_paired_opted_in
    def get(self):
        user = session.getCarl()
        self.response.out.write('{"success":0,"num_unread_messages":' + str(user.num_unread_messages) + ',"num_unread_sent_messages":' + str(user.num_unread_sent_messages) + '}')

class Send(webapp.RequestHandler):
    @functions.only_if_site_open
    @functions.only_if_paired_opted_in
    def post(self):
            source = session.getCarl()
            target = functions.get_user_by_CID(self.request.get("to"))
            if not target: self.response.out.write('{"success":2}') # check if user exists
            elif not functions.has_crush(source, target): self.response.out.write('{"success":3}') # you must have them as a crush
            elif not self.request.get("body"): self.response.out.write('{"success":4}') # message must have a body
            elif len(self.request.get("body")) > 500: self.response.out.write('{"success":5}') # message must be less than 500 characters
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
        if len(self.request.get("body")) > 500: # message must be less than 500 characters
            self.response.out.write('{"success":5}')
            return
            
        if self.request.get('body'):
            from datetime import datetime
            message = models.Message.get_by_id(long(self.request.get("mid"))) # maybe use key instead of key.id to find the message
            source = session.getCarl()
            if message and (message.source.carletonID == source.carletonID or message.target.carletonID == source.carletonID):
    
                reply = models.Reply()
                reply.message = message
    
                if message.source.carletonID == source.carletonID: # then we set the message.target as unread   
                    reply.source_unread = False
                    reply.message.target_any_unread = True
                    message.target.num_unread_messages += 1
                    message.target.put()
    
                elif message.target.carletonID == source.carletonID: # then we set the message.source as unread
                    reply.target_unread = False
                    reply.message.source_any_unread = True
                    message.source.num_unread_sent_messages += 1
                    message.source.put()
                    
                reply.source = source
                reply.body = self.request.get('body')
                reply.put()
                
                message.updated = datetime.now()
                message.source_deleted = False
                message.target_deleted = False
                message.put()
                
                self.response.out.write('{"success":0}') # success!
                
            else:
                self.response.out.write('{"success":2}') # message does not exist or trying to reply to someone else's message
        else:
            self.response.out.write('{"success":3}') # empty message body

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
            self.response.out.write('{"success":0}') # success!
        else:
            self.response.out.write('{"success":2}') # message not owned by the user or was deleted

class Report(webapp.RequestHandler):
    @functions.only_if_site_open
    @functions.only_if_paired_opted_in
    def post(self):
        message = models.Message.get_by_id(long(self.request.get("mid"))) # maybe use key instead of key.id to find the message                                                                                                                                           
        user = session.getCarl()
        if message and (message.source.carletonID == user.carletonID or message.target.carletonID == user.carletonID): # check if the user owns the message
            if message.source.carletonID == user.carletonID: # then the message.target is being reported
                emailfunctions.send_report(user, message.target, message)
            elif message.target.carletonID == user.carletonID: # then we set the message.source is being reported
                emailfunctions.send_report(user, message.source, message)
            self.response.out.write('{"success":0}') # success!
        else:
            self.response.out.write('{"success":2}') # message not owned by the user or was deleted
            
def get_unread_messages_for_user(user):
    return user.in_messages.filter("target_deleted =", False).filter("target_any_unread =", True).order("-updated")

def get_unread_messages_from_user(user):
    return user.out_messages.filter("source_deleted =", False).filter("source_any_unread =", True).order("-updated")

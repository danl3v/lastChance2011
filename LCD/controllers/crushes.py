from google.appengine.ext import webapp
from models import models
import session, view, functions

class Crushes(webapp.RequestHandler):
    @functions.only_if_paired_opted_in
    def get(self):
        site_status = functions.get_site_status()
        if site_status == "open":
            import random
            user = session.getCarl()
            crushes = get_crushes_for_user(user)
            messages = get_messages_for_user(user)
            sent_messages = get_messages_from_user(user)
            template_values = {
                'crushes': crushes,
                'messages': messages,
                'num_unread_messages': user.num_unread_messages,
                'num_unread_sent_messages': user.num_unread_sent_messages,
                'offset': random.randint(1, 100) - min([message.source.key().id() for message in messages]+[0]),
                'sent_messages': sent_messages,
                'current_page': { 'crushes': True }
                }
            view.renderTemplate(self, 'crushes.html', template_values)
            mark_messages_from_me_read(sent_messages)
            mark_messages_to_me_read(messages)
            
            user.num_unread_messages = 0
            user.num_unread_sent_messages = 0
            user.put()      
        elif site_status == "showing":
            template_values = {
                'matches': session.getCarl().in_matches,
                'current_page': { 'crushes': True }
                }
            view.renderTemplate(self, 'matches.html', template_values)
        else:
            self.redirect("/")

class AddCrush(webapp.RequestHandler):
    @functions.only_if_site_open
    @functions.only_if_paired_opted_in
    def post(self):
        source = session.getCarl()
        target = functions.get_user_by_CID(self.request.get("crush"))
        if functions.has_crush(source, target): self.response.out.write('{"success":2}') # cannot choose someone who is already a crush
        elif not target: self.response.out.write('{"success":3}') # crush must exist
        elif source.carletonID == target.carletonID: self.response.out.write('{"success":4}') # can't choose yourself as a crush (kind of weird that we need to compare their carletonIDs instead of just comparing them)
        elif len(get_crushes_for_user(source)) >= 5: self.response.out.write('{"success":5}') # can't have more than 5 crushes
        else:
            edge = models.Crush()
            edge.source = source
            edge.target = target
            edge.put()
            self.response.out.write('{"success":0, "status":"' + get_status(target) + '"}')   

class RemoveCrush(webapp.RequestHandler):
    @functions.only_if_site_open
    @functions.only_if_paired_opted_in
    def post(self):
        from datetime import datetime
        source = session.getCarl()
        target = functions.get_user_by_CID(self.request.get("crush"))
        crush = functions.has_crush(source, target)
        if crush:
            crush.deleted = True
            crush.deleted_time = datetime.now()
            crush.put()
            self.response.out.write('{"success":0}')
        else:
            self.response.out.write('{"success":2}')

class AutoFill(webapp.RequestHandler):
    @functions.only_if_site_open
    def get(self):
        users = models.Carl.all()
        users.order("first_name")
        results = users.fetch(1000) #if we have more than 1000 users, we need to fetch multiple times until we run out of fetches
        theJSON = ''.join([generate_JSON(user) for user in users])
        theJSON = "[" + theJSON[:-1] + "]"
        self.response.out.write(theJSON)

def generate_JSON(user):
    extra = " (opted-out)" if not user.opted_in else ""
    return '{"value":"' + user.first_name + ' ' + user.last_name + ' (' + user.carletonID + ')' + extra + '","carletonID":"' + user.carletonID + '","first_name":"' + user.first_name + '","last_name":"' + user.last_name + '"},'

def get_status(user):
    if not user.googleID: return "not_paired"
    elif not user.opted_in: return "opted_out"
    else: return "participating"

def get_crushes_for_user(user):
    #crushes = session.getCarl().in_crushes  # is the filter query or this property cheaper than next two lines?
    #crushes = models.Crush.all()
    #crushes.filter("source =", user)
    #crushes.filter("deleted =", False)
    return user.in_crushes.filter("deleted =", False).fetch(20) # there should not be more than 5

def get_messages_for_user(user): # need to somehow get messages by source
    #messages = models.Message.all()
    #messages.filter("target =", user)
    #messages.filter("target_deleted =", False)
    #messages.order("-updated")
    return user.out_messages.filter("target_deleted =", False).order("-updated")

def get_messages_from_user(user): # need to somehow get messages by source
    #messages = models.Message.all()
    #messages.filter("source =", user)
    #messages = user.in_messages
    return user.in_messages.filter("source_deleted =", False).order("-updated")
    #messages.order("-updated")
    #return messages

def mark_messages_from_me_read(messages):
    for message in messages:
        for reply in message.replies:
            reply.source_unread = False
            reply.put()

def mark_messages_to_me_read(messages):
    for message in messages:
        message.target_unread = False
        message.put()
        for reply in message.replies:
            reply.target_unread = False
            reply.put()



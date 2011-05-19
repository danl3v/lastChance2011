from google.appengine.ext import webapp
import session, models, view, functions

class Crushes(webapp.RequestHandler):
    def get(self):
        if session.isPaired() and session.opted_in():
            crushes = get_crushes_for_user(session.getCarl())
            messages = get_messages_for_user(session.getCarl())
            sent_messages = get_messages_from_user(session.getCarl())
            template_values = {
                'crushes': crushes,
                'messages': messages,
                'sent_messages': sent_messages,
                'current_page': { 'crushes': True }
                }
            view.renderTemplate(self, 'crushes.html', template_values)
        else:
            self.response.out.write('Your account must be paired and opted-in before adding crushes. Go to <a href="/settings">settings</a> to resolve this issue.')

class AddCrush(webapp.RequestHandler):
    def post(self):
        if session.isPaired() and session.opted_in():
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
        else:
            self.response.out.write('{"success":1}')    

class RemoveCrush(webapp.RequestHandler):
    def post(self):
        if session.isPaired() and session.opted_in():
            source = session.getCarl()
            target = functions.get_user_by_CID(self.request.get("crush"))
            crush = functions.has_crush(source, target)
            if crush:
                crush.delete()
                self.response.out.write('{"success":0}')
            else:
                self.response.out.write('{"success":2}')
        else:
            self.response.out.write('{"success":1}')

class AutoFill(webapp.RequestHandler):
    def get(self):
        users = models.Carl.all()
        users.order("first_name")
        results = users.fetch(1000) #if we have more than 1000 users, we need to fetch multiple times until we run out of fetches
        theJSON = ''.join(['{"value":"' + user.first_name + ' ' + user.last_name + ' (' + user.carletonID + ')","carletonID":"' + user.carletonID + '","first_name":"' + user.first_name + '","last_name":"' + user.last_name + '"},' for user in users])
        theJSON = "[" + theJSON[:-1] + "]"
        self.response.out.write(theJSON)

def get_status(user):
    if not user.googleID: return "not_paired"
    elif not user.opted_in: return "opted_out"
    else: return "available"

def get_crushes_for_user(user):
    crushes = models.Crush.all()
    crushes.filter("source =", user)
    return crushes.fetch(20) # there should not be more than 5

def get_messages_for_user(user): # need to somehow get messages by source
    messages = models.Message.all()
    messages.filter("target =", user)
    messages.filter("target_deleted =", False)
    messages.order("-updated")
    return messages.fetch(1000) # if we have more than 1000 messages, we need to fetch multiple times

def get_messages_from_user(user): # need to somehow get messages by source
    messages = models.Message.all()
    messages.filter("source =", user)
    messages.filter("source_deleted =", False)
    messages.order("-updated")
    return messages.fetch(1000) # if we have more than 1000 messages, we need to fetch multiple times

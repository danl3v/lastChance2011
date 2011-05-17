from google.appengine.ext import webapp
import session, models, view, functions

class Crushes(webapp.RequestHandler):
    def get(self):
        if session.isPaired() and session.is_active():
            carleton_id = session.getCarl().carletonID
            crushes = get_crushes_for_user(carleton_id)
            messages = get_messages_by_CID(carleton_id)
            template_values = {
                'crushes': crushes,
                'messages': messages,
                'current_page': { 'crushes': True }
                }
            view.renderTemplate(self, 'crushes.html', template_values)
        else:
            self.response.out.write('Your account must be paired and opted-in before adding crushes. Go to <a href="/settings">settings</a> to resolve this issue.')

class AddCrush(webapp.RequestHandler):
    def post(self):
        if session.isPaired() and session.is_active():
            carleton_id = session.getCarl().carletonID
            if functions.has_crush(carleton_id, self.request.get("crush")): self.response.out.write('{"success":2}') # cannot choose someone who is already a crush
            elif not functions.get_user_by_CID(self.request.get("crush")): self.response.out.write('{"success":3}') # crush must exist
            elif carleton_id == self.request.get("crush"): self.response.out.write('{"success":4}') # can't choose yourself as a crush
            elif len(get_crushes_for_user(carleton_id)) >= 5: self.response.out.write('{"success":5}') # can't have more than 5 crushes
            else:
                crush = functions.get_user_by_CID(self.request.get("crush"))
                if not crush.googleID: status = "not_paired"
                elif not crush.active: status = "opted_out"
                else: status = "available"
                
                edge = models.Carl2Carl()
                edge.source = carleton_id
                edge.target = self.request.get('crush')
                edge.put()
                self.response.out.write('{"success":0, "status":"' + status + '"}')
        else:
            self.response.out.write('{"success":1}')    

class RemoveCrush(webapp.RequestHandler):
    def post(self):
        if session.isPaired() and session.is_active():
            carleton_id = session.getCarl().carletonID
            carl = functions.has_crush(carleton_id, self.request.get("crush"))
            carl.delete()
            self.response.out.write('{"success":0}')
        else:
            self.response.out.write('{"success":1}')

class AutoFill(webapp.RequestHandler):
    def get(self):
        users = models.Carl.all()
        users.order("first_name")
        results = users.fetch(1000) #if we have more that 1000 users, we need to fetch multiple times until we run out of fetches

        theJSON = ''.join(['{"value":"' + user.first_name + ' ' + user.last_name + ' (' + user.carletonID + ')","carletonID":"' + user.carletonID + '","first_name":"' + user.first_name + '","last_name":"' + user.last_name + '"},' for user in users])

        theJSON = "[" + theJSON[:-1] + "]"
        self.response.out.write(theJSON)

def get_crushes_for_user(user):
    carl2carl = models.Carl2Carl.all()
    carl2carl.filter("source =", user)
    results = carl2carl.fetch(20) # there should not be more than 5
    return [functions.get_user_by_CID(result.target) for result in results]

def get_messages_by_CID(carleton_id):
    messages = models.Message.all()
    messages.filter("target =", carleton_id)
    messages.filter("deleted =", False)
    messages.order("-created")
    return messages.fetch(1000)

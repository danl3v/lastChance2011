from google.appengine.ext import webapp
from models import models
import functions, emailfunctions

class NotifyCrushes(webapp.RequestHandler):
    def get(self):
        crushes = models.Crush.all()
        crushes.filter("notified =", False)
        crushes_to_notify = {}
        for crush in crushes:
            if crush.target.carletonID not in crushes_to_notify:
                crushes_to_notify[crush.target.carletonID] = [0, crush.target]
            crushes_to_notify[crush.target.carletonID][0] += 1
            crush.notified = True
            crush.put()
        for crush in crushes_to_notify:
            emailfunctions.send_crushed_upon(crushes_to_notify[crush][1], crushes_to_notify[crush][0])

class UpdateMatches(webapp.RequestHandler):
    def get(self):
        functions.update_matches()

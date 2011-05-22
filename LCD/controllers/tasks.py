from google.appengine.ext import webapp
from models import models
import functions

class NotifyCrushes(webapp.RequestHandler):
    def get(self):
        crushes = models.Crush.all()
        crushes.filter("notified =", False)

        notify_dict = {}

        for crush in crushes:
            
            if crush.target.carletonID not in notify_dict:
                notify_dict[crush.target.carletonID] = 0
            notify_dict[crush.target.carletonID] += 1
            crush.notified = True
            crush.put()
            # send out notifcations
            
        self.response.out.write(notify_dict)

class UpdateMatches(webapp.RequestHandler):
    def get(self):
        functions.update_matches()

from google.appengine.ext import webapp
from models import models
import session, view, functions

class NotifyCrushes(webapp.RequestHandler):
    def get(self):
        self.response.out.write("asdfasdf")
        crushes = models.Crush.all()
        #crushes.filter("notified =", False)

        notify_dict = {}

        for crush in crushes:
            '''
            if crush.carletonID not in notify_dict:
                notify_dict[crush.carletonID] = []
            notify_dict[crush.carletonID].append(crush.target)
            #crush.notified = True
            #crush.put()
            '''
            self.response.out.write(crush.target.first_name)
            self.response.out.write(crush.notified)
        self.response.out.write(notify_dict)
        self.response.out.write("done")

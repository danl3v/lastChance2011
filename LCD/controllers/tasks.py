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
            
class UpdateStatistics(webapp.RequestHandler):
    def get(self):
    
        matches = functions.update_matches()
        num_crushes = models.Crush.all().count()
        num_messages = models.Message.all().count()
        num_replies = models.Reply.all().count()
        num_matches = len(matches) / 2
        num_paired = models.Carl.all().filter("googleID !=", None).count()
        num_opted_out = models.Carl.all().filter("opted_in =", False).count()
        num_to_pair = models.Carl.all().count() - num_paired

        functions.set_statistic("num_crushes", num_crushes)
        functions.set_statistic("num_messages", num_messages)
        functions.set_statistic("num_replies", num_replies)
        functions.set_statistic("num_matches", num_matches)
        functions.set_statistic("num_paired", num_paired)
        functions.set_statistic("num_opted_out", num_opted_out)
        functions.set_statistic("num_to_pair", num_to_pair)
        
        self.response.out.write('{"success":0}')
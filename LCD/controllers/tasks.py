from google.appengine.ext import webapp
from models import models
import functions, emailfunctions

class SendDigest(webapp.RequestHandler):
    def get(self):
        users = models.Carl.all()
        for user in users:
            num_crushes = user.out_crushes.filter("notified =", False).count()
            num_messages = user.num_unread_messages
            if (num_crushes or num_messages) and user.opted_in:
                emailfunctions.send_digest(user, num_crushes, num_messages)
                for crush in user.in_crushes:
                    crush.notified = True
                    #****crush.put()
            
class UpdateStatistics(webapp.RequestHandler):
    def get(self):
    
        matches = functions.update_matches()
        num_crushes = models.Crush.all().filter("deleted =", False).count()
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
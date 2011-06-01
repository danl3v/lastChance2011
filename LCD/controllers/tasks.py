from google.appengine.ext import webapp
from models import models
import functions, emailfunctions

class SendDigest(webapp.RequestHandler):
    def get(self):
        if functions.get_site_status() == 'open':
            users = models.Carl.all()
            for user in users:
                out_crushes = user.out_crushes.filter("deleted =", False).filter("notified =", False)
                num_crushes = out_crushes.count()
                num_messages = user.num_unread_messages + user.num_unread_sent_messages
                if (num_crushes or num_messages) and user.opted_in:
                    emailfunctions.send_digest(user, num_crushes, num_messages)
                    for crush in out_crushes:
                        crush.notified = True
                        crush.put()
            
class UpdateStatistics(webapp.RequestHandler):
    def get(self):
    
        matches = functions.update_matches()
        num_users_with_matches = functions.num_users_with_matches()
        num_crushes = models.Crush.all().filter("deleted =", False).count()
        num_messages = models.Message.all().count()
        num_replies = models.Reply.all().count()
        num_matches = len(matches) / 2
        num_paired = models.Carl.all().filter("googleID !=", None).count()
        num_opted_out = models.Carl.all().filter("opted_in =", False).count()
        num_to_pair = models.Carl.all().count() - num_paired
        num_users_crushing = sum([1 for carl in models.Carl.all() if carl.in_crushes.filter("deleted =", False).count() > 0])
        num_users_crushed_on = sum([1 for carl in models.Carl.all() if carl.out_crushes.filter("deleted =", False).count() > 0])

        functions.set_statistic("num_crushes", num_crushes)
        functions.set_statistic("num_messages", num_messages)
        functions.set_statistic("num_replies", num_replies)
        functions.set_statistic("num_matches", num_matches)
        functions.set_statistic("num_users_with_matches", num_users_with_matches)
        functions.set_statistic("num_paired", num_paired)
        functions.set_statistic("num_opted_out", num_opted_out)
        functions.set_statistic("num_to_pair", num_to_pair)
        functions.set_statistic("num_users_crushing", num_users_crushing)
        functions.set_statistic("num_users_crushed_on", num_users_crushed_on)
        
        self.response.out.write('{"success":0}')

class OpenSite(webapp.RequestHandler): # open the site on may 27, 2011
    def get(self):
        local_time = functions.get_local_time()
        if local_time.day == 27 and local_time.month == 5 and local_time.year == 2011:
            # maybe send invites here?
            functions.set_site_status('open')
        
class CloseSite(webapp.RequestHandler): # close the site on jun 7, 2011
    def get(self):
        local_time = functions.get_local_time()
        if local_time.day == 7 and local_time.month == 6 and local_time.year == 2011:
            functions.set_site_status('calculating')

class ShowMatches(webapp.RequestHandler): # show the matches on jun 7, 2011
    def get(self):
        local_time = functions.get_local_time()
        if local_time.day == 7 and local_time.month == 6 and local_time.year == 2011:
            functions.update_matches()
            # maybe send emails here?
            functions.set_site_status('showing')


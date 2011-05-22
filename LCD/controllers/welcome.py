from google.appengine.ext import webapp

from models import models
import view, session, emailfunctions

class MainPage(webapp.RequestHandler):
    def get(self):

        num_paired = models.Carl.all().filter("googleID !=", None).count()
        num_opted_out = models.Carl.all().filter("opted_in =", False).count()
        num_to_pair = models.Carl.all().count() - num_paired

        template_values = {
            'current_page': {'main': True},
            'num_crushes': models.Crush.all().count(),
            'num_messages': models.Message.all().count(),
            'num_replies': models.Reply.all().count(),
            'num_matches': models.Match.all().count() / 2,
            'num_paired': num_paired,
            'num_opted_out': num_opted_out,
            'num_to_pair': num_to_pair
            }
        view.renderTemplate(self, 'index.html', template_values)

class Contact(webapp.RequestHandler):
    def get(self):
        user = session.get_current_user()
        template_values = {
            'user': user
            }
        view.renderTemplate(self, 'contact.html', template_values)
    def post(self):
        emailfunctions.send_contact_form(self.request.get("subject"), self.request.get("body"), self.request.get("anonymous"))
        template_values = {}
        view.renderTemplate(self, 'contact_success.html', template_values)

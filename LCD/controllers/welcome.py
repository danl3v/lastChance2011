from google.appengine.ext import webapp

from models import models
import view, session, functions, emailfunctions

class MainPage(webapp.RequestHandler):
    def get(self):
        from datetime import datetime, timedelta
        template_values = {
            'current_page': {'main': True},
            'num_crushes': functions.get_statistic('num_crushes'),
            'num_messages': functions.get_statistic('num_messages'),
            'num_replies': functions.get_statistic('num_replies'),
            'num_matches': functions.get_statistic('num_matches'),
            'num_users_with_matches': functions.get_statistic('num_users_with_matches'),
            'num_paired': functions.get_statistic('num_paired'),
            'num_opted_out': functions.get_statistic('num_opted_out'),
            'num_to_pair': functions.get_statistic('num_to_pair'),
            'num_users_crushing': functions.get_statistic('num_users_crushing'),
            'num_users_crushed_on': functions.get_statistic('num_users_crushed_on'),
            'time_now': functions.get_local_time()
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

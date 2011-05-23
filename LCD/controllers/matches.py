from google.appengine.ext import webapp
from models import models
import session, view, functions

class Matches(webapp.RequestHandler):
    @functions.only_if_site_showing
    def get(self):
        if session.isPaired() and session.opted_in():
            template_values = {
                'matches': session.getCarl().matches.fetch(10),
                'current_page': { 'matches': True }
                }
            view.renderTemplate(self, 'matches.html', template_values)
        else:
            self.response.out.write('Your account must be paired and opted-in in order to view matches. Go to <a href="/settings">settings</a> to resolve this issue.')
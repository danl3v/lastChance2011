import logging, email
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import mail

class alertTheAdmins(InboundMailHandler):
    def receive(self, message):
        #Ugh I don't know [ send it to contact@lastchance2011.com]


application = webapp.WSGIApplication([alertTheAdmins.mapping()], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

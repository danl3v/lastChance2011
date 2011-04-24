import logging, email
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import mail

class sendEmailToC(InboundMailHandler):
    def receive(self, mail_message):
        # I'm pretty sure that InboundEmailMessage objects
        # work just like regular EmailMessage objects,
        # so we should be able to just forward them
        # to the appropriate place.

        #c = "conrad.p.dean@gmail.com"
        #mail_message.to = c
        #mail_message.send()

        forward = mail.EmailMessage()
        #forward.sender = mail_message.sender # for some reason this thing makes it broken.  "invalidsendererror"
        forward.sender = "C <c@lcdance2011.appspotmail.com>"
        forward.to = "conrad.p.dean@gmail.com"
        forward.subject = mail_message.subject
        forward.body = "original sender:"+ mail_message.sender +" Original message: " + mail_message.body.decode()
        forward.send()


        reassurance = mail.EmailMessage()
        reassurance.sender = "C <c@lcdance2011.appspotmail.com>"
        reassurance.to = mail_message.sender
        reassurance.subject = "automatic response"
        reassurance.body = """
Your message has been passed along to a real person.

They will never respond to you, but they'll nonetheless read your email.
"""
        reassurance.send()

application = webapp.WSGIApplication([sendEmailToC.mapping()], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

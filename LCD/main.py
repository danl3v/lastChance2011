from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import crushes, settings, messages

def main():
    application = webapp.WSGIApplication([
           ('/crushes/add', crushes.AddCrush),
           ('/crushes/remove', crushes.RemoveCrush),
           ('/crushes', crushes.Crushes),
           ('/autofill', crushes.AutoFill),
           ('/settings', settings.Settings),
           ('/pair/(.*)/(.*)', settings.AutoPair),
           ('/settings/(.*)', settings.Settings),
           ('/messages/send', messages.Send),
           ('/messages/delete', messages.Delete)
         ],debug=True)

    run_wsgi_app(application)

if __name__ == "__main__":
    main()

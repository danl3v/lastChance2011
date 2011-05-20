from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from controllers import crushes, settings, messages, welcome, admin

def main():
    application = webapp.WSGIApplication([
           ('/', welcome.MainPage),
           ('/contact', welcome.Contact),
           ('/crushes/add', crushes.AddCrush),
           ('/crushes/remove', crushes.RemoveCrush),
           ('/crushes', crushes.Crushes),
           ('/autofill', crushes.AutoFill),
           ('/settings', settings.Settings),
           ('/pair/(.*)/(.*)', settings.AutoPair),
           ('/settings/(.*)', settings.Settings),
           ('/messages/send', messages.Send),
           ('/messages/reply', messages.Reply),
           ('/messages/delete', messages.Delete),
           ('/admin', admin.Admin),
           ('/admin/', admin.Admin),
           ('/admin/addcarl', admin.AddCarl),
           ('/admin/addusers', admin.AddUsers),
           ('/admin/newpaircode', admin.NewPairCode),
           ('/admin/deletecarl', admin.DeleteCarl),
           ('/admin/invite', admin.Invite),
           ('/admin/unpaircarl', admin.UnPairCarl),
           ('/admin/calculate', admin.CalculateCrushes)
         ],debug=True)

    run_wsgi_app(application)

if __name__ == "__main__":
    main()

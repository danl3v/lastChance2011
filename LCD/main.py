from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from controllers import crushes, settings, messages, welcome, admin, tasks

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
           ('/settings/invite', settings.Invite),
           ('/settings/(.*)', settings.Settings),
           ('/messages/get', messages.Get),
           ('/messages/send', messages.Send),
           ('/messages/reply', messages.Reply),
           ('/messages/delete', messages.Delete),
           ('/messages/report_abuse', messages.Report),
           ('/admin', admin.Admin),
           ('/admin/', admin.Admin),
           ('/admin/addusers', admin.AddUsers),
           ('/admin/newpaircode', admin.NewPairCode),
           ('/admin/deletecarl', admin.DeleteCarl),
           ('/admin/invite', admin.Invite),
           ('/admin/invite_all', admin.InviteAll),
           ('/admin/invite_not_paired', admin.InviteNotPaired),
           ('/admin/unpaircarl', admin.UnPairCarl),
           ('/admin/send_match_notifications', admin.SendMatchNotifications),
           ('/admin/set_site_status', admin.SetSiteStatus),
           ('/tasks/send_digest', tasks.SendDigest),
           ('/tasks/update_matches', tasks.UpdateMatches),
           ('/tasks/update_statistics', tasks.UpdateStatistics),
           ('/tasks/open', tasks.OpenSite),
           ('/tasks/close', tasks.CloseSite),
           ('/tasks/show', tasks.ShowMatches)
         ],debug=True)

    run_wsgi_app(application)

if __name__ == "__main__":
    main()

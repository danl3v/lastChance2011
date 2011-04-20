import os
from google.appengine.ext.webapp import template

import session

def getNavData(self):
    user = session.get_current_user()
    if user:
        login_url = session.create_logout_url(self.request.uri)
        login_url_linktext = 'Logout'
        
        if session.isPaired():
            pair_url = "pair"
            pair_url_linktext = "Unpair Your Account"
        else:
            pair_url = "pair"
            pair_url_linktext = "You need to pair your account"
    else:
        login_url = session.create_login_url(self.request.uri)
        login_url_linktext = 'Login'
        pair_url = ""
        pair_url_linktext = ""
        
    if session.is_current_user_admin():
        admin = True
    else:
        admin = False

    template_values =  {
        'user': user,
        'admin': admin,
        'login_url': login_url,
        'login_url_linktext': login_url_linktext,
        'pair_url': pair_url,
        'pair_url_linktext': pair_url_linktext
        }

    return template_values

def renderTemplate(self, template_file, template_values):

    template_values = dict(getNavData(self), **template_values)

    path = os.path.join(os.path.dirname(__file__), 'templates/header.html')
    self.response.out.write(template.render(path, template_values))
    
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_file)
    self.response.out.write(template.render(path, template_values))
    
    path = os.path.join(os.path.dirname(__file__), 'templates/footer.html')
    self.response.out.write(template.render(path, template_values))


import os
from google.appengine.ext.webapp import template

import session

def getHeaderFooterData(self):
    '''
    gets and returns the template values to render the header and footer, which are standard on all pages
    '''
    user = session.get_current_user()
    if user:
        login_url = session.create_logout_url(self.request.uri)
        login_url_linktext = 'Logout'
        carl = session.getCarl()  # Can only be run when session.get_current_user() != False
        
        if session.isPaired():
            paired = True
            pair_url_linktext = "Unpair Account With " + carl.carletonID.title()
        else:
            paired = False
            pair_url_linktext = "You Need to Pair Your Account"
        
        if session.is_active():
            active = True
            active_url_linktext = "Opt Out"
        else:
            active = False
            active_url_linktext = "Opt In"

    else:
        login_url = session.create_login_url(self.request.uri)
        login_url_linktext = 'Login'
        paired = False
        pair_url_linktext = ""
        active = False
        active_url_linktext = ""
        
    if session.is_current_user_admin():
        admin = True
    else:
        admin = False

    template_values =  {
        'user': user,
        'admin': admin,
        'login_url': login_url,
        'login_url_linktext': login_url_linktext,
        'paired': paired,
        'pair_url_linktext': pair_url_linktext,
        'active': active,
        'active_url_linktext': active_url_linktext

        }

    return template_values

def renderTemplate(self, template_file, template_values):

    template_values = dict(getHeaderFooterData(self), **template_values)

    path = os.path.join(os.path.dirname(__file__), 'templates/header.html')
    self.response.out.write(template.render(path, template_values))
    
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_file)
    self.response.out.write(template.render(path, template_values))
    
    path = os.path.join(os.path.dirname(__file__), 'templates/footer.html')
    self.response.out.write(template.render(path, template_values))


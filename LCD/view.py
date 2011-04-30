import os
from google.appengine.ext.webapp import template

import session

def getHeaderFooterData(self):
    '''
    gets and returns the template values to render the header and footer, which are standard on all pages
    '''
    user = session.get_current_user()
    carleton_id = None
    if user:
        login_url = session.create_logout_url("/")
        login_url_linktext = 'Logout'
        active = session.is_active()        
        if session.isPaired():
            paired = True
            carleton_id = session.getCarl().carletonID
        else: paired = False
    else:
        login_url = session.create_login_url(self.request.uri)
        login_url_linktext = 'Login'
        paired = False
        active = False
        
    admin = session.is_current_user_admin()

    template_values =  {
        'user': user,
        'carleton_id': carleton_id,
        'admin': admin,
        'login_url': login_url,
        'login_url_linktext': login_url_linktext,
        'paired': paired,
        'active': active,
        }

    return template_values

def renderTemplate(self, template_file, template_values):
    template_values = dict(getHeaderFooterData(self), **template_values)
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_file)
    self.response.out.write(template.render(path, template_values))


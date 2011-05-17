import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext.webapp import template

import models, session

def getHeaderFooterData(self):
    '''
    gets and returns the template values to render the header and footer, which are standard on all pages
    '''
    user = session.get_current_user()
    carleton_id = None
    first_name = None
    last_name = None
    num_crushes = models.Carl2Carl.all().count()
    if user:
        login_url = session.create_logout_url("/")
        login_url_linktext = 'Logout'
        opted_in = session.opted_in()        
        if session.isPaired():
            paired = True
            carl = session.getCarl()
            carleton_id = carl.carletonID
            first_name = carl.first_name
            last_name = carl.last_name
        else: paired = False
    else:
        login_url = session.create_login_url(self.request.uri)
        login_url_linktext = 'Login'
        paired = False
        opted_in = False
        
    admin = session.is_current_user_admin()

    template_values =  {
        'user': user,
        'carleton_id': carleton_id,
        'first_name': first_name,
        'last_name': last_name,
        'admin': admin,
        'login_url': login_url,
        'login_url_linktext': login_url_linktext,
        'paired': paired,
        'opted_in': opted_in,
        'num_crushes': num_crushes
        }

    return template_values

def renderTemplate(self, template_file, template_values):
    template_values = dict(getHeaderFooterData(self), **template_values)
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_file)
    self.response.out.write(template.render(path, template_values))


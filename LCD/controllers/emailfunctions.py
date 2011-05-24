import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.api import mail
from google.appengine.ext.webapp import template

import session

last_chance_dance_email_address = "Last Chance Dance <contact@lastchance2011.com>" # this is our email
subject_prefix = "[lcD 2011] "

def render_email_body(template_file, template_values):
    '''
    Renders the body of an email.
    '''
    path = os.path.join(os.path.dirname(__file__), '../email_templates/' + template_file)
    return template.render(path, template_values)

def send_invitation(carletonAccount):
    '''
    Sends an invitation.
    '''
    user_address = carletonAccount.carletonID + "@carleton.edu"

    sender_address = last_chance_dance_email_address
    subject = subject_prefix + "Invitation!"

    template_values = { 'user': carletonAccount }
    body = render_email_body('invitation.html', template_values)
    
    mail.send_mail(sender_address, user_address, subject, body)

def send_digest(carletonAccount, num_crushes, num_messages):
    '''
    Sends an email to a user who has been chosen by someone else.
    '''
    user_address = carletonAccount.carletonID + "@carleton.edu"
    sender_address = last_chance_dance_email_address
    subject = subject_prefix + "Daily Digest"
    
    template_values = {
           'first_name': carletonAccount.first_name,
           'num_crushes': num_crushes,
           'num_messages': num_messages
           }
    body = render_email_body('digest.html', template_values)
    
    mail.send_mail(sender_address, user_address, subject, body)

def send_matches(carletonAccount, matches):
    '''
    Sends matches
    '''
    user_address = carletonAccount.carletonID + "@carleton.edu"
    sender_address = last_chance_dance_email_address
    subject = subject_prefix + "Here are your matches..."
    
    template_values = {
           'carletonAccount': carletonAccount,
           'matches': matches
           }
    body = render_email_body('match.html', template_values)
    
    mail.send_mail(sender_address, user_address, subject, body)

def send_contact_form(subject, body, anonymous):
    '''
    Sends a contact form.
    '''
    to_address = last_chance_dance_email_address
    if session.get_current_user() and not anonymous:
        from_address = session.get_current_user().email()
        subject = subject_prefix + "[Feedback] " + subject
    else:
        from_address = last_chance_dance_email_address
        subject = subject_prefix + "[Feedback] [Anonymous] " + subject
    
    mail.send_mail(from_address, to_address, subject, body)

def send_paired(carletonAccount, googleAccount):
    '''
    Sends a notification that an account was paired
    '''
    from_address = last_chance_dance_email_address
    to_address = carletonAccount.carletonID + "@carleton.edu"
    subject = subject_prefix + "Account Paired"

    template_values = { 'carletonAccount': carletonAccount,
                        'googleAccount': googleAccount
                        }
    body = render_email_body('paired_notification.html', template_values)

    mail.send_mail(from_address, to_address, subject, body)


def send_unpaired(carletonAccount, googleAccount):
    '''
    Sends a notification that an account was unpaired
    '''
    from_address = last_chance_dance_email_address
    to_address = carletonAccount.carletonID + "@carleton.edu"
    subject = subject_prefix + "Account Un-Paired"

    template_values = { 'carletonAccount': carletonAccount,
                        'googleAccount': googleAccount
                        }
    body = render_email_body('unpaired_notification.html', template_values)

    mail.send_mail(from_address, to_address, subject, body)

def send_opted_out(source, target):
    '''
    Sends a notification that someone opted out. source and target are Carl objects.
    '''
    from_address = last_chance_dance_email_address
    to_address = source.carletonID + "@carleton.edu"
    subject = subject_prefix + "Crush Opted Out"

    template_values = { 'source': source,
                        'target': target
                        }
    body = render_email_body('opted_out_notification.html', template_values)

    mail.send_mail(from_address, to_address, subject, body)

def send_opted_in(source, target):
    '''
    Sends a notification that someone opted back in. source and target are Carl objects.
    '''
    from_address = last_chance_dance_email_address
    to_address = source.carletonID + "@carleton.edu"
    subject = subject_prefix + "Crush Opted Back In!"

    template_values = { 'source': source,
                        'target': target
                        }
    body = render_email_body('opted_in_notification.html', template_values)

    mail.send_mail(from_address, to_address, subject, body)

from google.appengine.api import mail
from google.appengine.ext.webapp import template
import session, os

last_chance_dance_email_address = "Last Chance Dance <contact@lastchance2011.com>" # this is our email

def renderEmailBody(template_file, template_values):
    '''
    Renders the body of an email.
    '''
    path = os.path.join(os.path.dirname(__file__), 'email_templates/' + template_file)
    return template.render(path, template_values)

def sendInvite(carletonAccount):
    '''
    Sends an invitation.
    '''
    username = carletonAccount.carletonID
    verificationCode = carletonAccount.verificationCode

    #user_address = carletonAccount.carletonID + "@carleton.edu"
    user_address = ["conrad.p.dean@gmail.com", "dlouislevy@gmail.com"]

    sender_address = last_chance_dance_email_address
    subject = "[Carleton Last Chance Dance 2011] Invitation!"

    template_values = {
        'carleton_id': carletonAccount.carletonID,
        'pair_code': verificationCode
        }
    body = renderEmailBody('invitation.html', template_values)
    
    mail.send_mail(sender_address, user_address, subject, body)

def sendPersonChosen(carletonID):
    '''
    Sends an email to a user who has been chosen by someone else.
    '''

    #user_address = carletonID + "@carleton.edu"
    user_address = ["conrad.p.dean@gmail.com", "dlouislevy@gmail.com"]

    sender_address = last_chance_dance_email_address
    subject = "[Carleton Last Chance Dance 2011] Someone Chose You as a Crush"
    
    template_values = { 'carletonID': carletonID }
    body = renderEmailBody('you_have_been_crushed_notification.html', template_values)
    
    mail.send_mail(sender_address, user_address, subject, body)

def sendContactForm(subject, body, anonymous):
    '''
    Sends a contact form.
    '''
    to_address = last_chance_dance_email_address
    if session.get_current_user() and not anonymous:
        from_address = session.get_current_user().email()
        subject = "[LCD Feedback] " + subject
    else:
        from_address = last_chance_dance_email_address
        subject = "[LCD Feedback] [Anonymous] " + subject
    
    mail.send_mail(from_address, to_address, subject, body)

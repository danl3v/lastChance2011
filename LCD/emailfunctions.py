from google.appengine.api import mail
import session

def sendInvite(carletonAccount):
    username = carletonAccount.carletonID
    verificationCode = carletonAccount.verificationCode

    #user_address = carletonAccount.carletonID + "@carleton.edu"
    user_address = ["conrad.p.dean@gmail.com", "dlouislevy@gmail.com"]

    sender_address = "Conerd <conrad.p.dean@gmail.com>"  # figure out a more legit email (our app can receive email, so let's do that or create a gmail
    subject = "[Carleton Last Chance Dance 2011] Invitation!"
    body = """
Hey there!

You've been invited to Carleton Last Chance Dance.

To open your account, go to http://lcdance2011.appspot.com/ with the paircode below.

Carleton Account: %s
Pair Code:        %s

After logging in with your Gmail account, you will be prompted to pair your account with your carleton account using the pair code above.

Have fun, and remember: If you can't handle the heat, stay out of the sex kitchen.

Nursing seared genitalia,
Last Chance Dance 2011
""" % (username,verificationCode)
    
    mail.send_mail(sender_address, user_address, subject, body)

def sendPersonChosen(carletonID):
    '''
    Sends an email to a user who has been chosen by someone else.
    '''

    #user_address = carletonID + "@carleton.edu"
    user_address = ["conrad.p.dean@gmail.com", "dlouislevy@gmail.com"]

    sender_address = "Conerd <conrad.p.dean@gmail.com>"  # figure out a more legit email (our app can receive email, so let's do that or create a gmail
    subject = "[Carleton Last Chance Dance 2011] Someone Chose You as a Crush"
    body = """
Hey there %s!

Someone selected you as a crush on Carleton Last Chance Dance 2011

You can select your own crushes at http://lcdance2011.appspot.com/.

Have fun, and remember: If you can't handle the heat, stay out of the sex kitchen.

Nursing seared genitalia,
Last Chance Dance 2011
""" % (carletonID)
    
    mail.send_mail(sender_address, user_address, subject, body)

def sendContactForm(subject, body):
    '''
    Sends a contact form.
    '''
    to_address = "contact@lastchance2011.com"
    if session.get_current_user():
        from_address = session.get_current_user().email()
        subject = "[LCD Feedback] " + subject
    else:
        from_address = "contact@lastchance2011.com"
        subject = "[LCD Feedback] [Anonymous] " + subject
    
    mail.send_mail(from_address, to_address, subject, body)

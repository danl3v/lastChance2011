from google.appengine.api import mail

def sendInvite(carletonAccount):
    username = carletonAccount.carletonID
    verificationCode = carletonAccount.verificationCode

    #user_address = carletonAccount.carletonID + "@carleton.edu"
    user_address = ["conrad.p.dean@gmail.com", "dlouislevy@gmail.com"]

    sender_address = "Conerd <conrad.p.dean@gmail.com>"  # figure out a more legit email (our app can receive email, so let's do that or create a gmail
    subject = "Last Chance Dance Invitation!"
    body = """
Hey there!
You've been invited to this year's Last Chance Dance.

To open your account, go to http://lcdance2011.appspot.com/ with the paircode below.

Carleton Account: %s
Pair Code:        %s

After logging in with your Gmail account, you will be prompted to verify your account with the pair code above.

Have fun, and remember: If you can't handle the heat, stay out of the sex kitchen.

Nursing seared genitalia,
C
""" % (username,verificationCode)
    
    mail.send_mail(sender_address, user_address, subject, body)

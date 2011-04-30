
import models, session

def sendMessage(target,message):
    newMessage = models.Message()
    newMessage.source = session.getCarl().carletonID
    newMessage.target = target
    newMessage.message = message
    newMessage.read = False
    newMessage.put()

from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import users


class XMPPHandler(webapp.RequestHandler):
    
    def post(self):
       
        message = xmpp.Message(self.request.POST)
        try:
            user = User.get_by_key_name(message.sender)
            
            if(user is None): #If new user
            
                user = User(key_name=message.sender,
                            firstTime=False, email=message.sender, returningSequence = 0)
                user.put()
                message.reply("Welcome to the Calendar Adder")
                
            else: #If returning member
                
                returningSequence = user.returningSequence
                
                if returningSequence == 0:
                    message.reply("Welcome back!")
                    message.reply("Event Name?")
                    returningSequence +=1
                elif returningSequence == 1:
                    event = message.body
                    message.reply("Date?")
                    returningSequence +=1
                elif returningSequence == 2:
                    date = message.body
                    message.reply("Time?")
                    returningSequence +=1
                elif returningSequence == 3:
                    time = message.body
                    message.reply("Event Added")
                    returningSequence = 0
                else:
                    message.reply("Something went wrong!! " + str(returningSequence))

                user.returningSequence = returningSequence
                user.put() 
                                        

        except db.BadKeyError:
            message.reply("FATAL ERROR!")
                


class User(db.Model):
    name = db.StringProperty()
    email = db.StringProperty()
    firstTime = db.BooleanProperty()
    returningSequence = db.IntegerProperty()
    

application = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

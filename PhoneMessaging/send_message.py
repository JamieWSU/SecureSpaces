from twilio.rest import Client 
import apiKeys as keys
message = input("Enter your message: ") 
# Your Account SID from twilio.com/console
# Your Auth Token from twilio.com/console

client = Client(keys.account_sid, keys.auth_token)

message = client.messages.create(
    to="+15093080228",
    from_="+12055767590",
    body=message)

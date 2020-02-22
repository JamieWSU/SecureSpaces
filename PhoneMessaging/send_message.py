from twilio.rest import Client
message = raw_input("Enter your message: ") 
# Your Account SID from twilio.com/console
account_sid = "AC0e9ca8edcd3824bc731e0cb7388659e0"
# Your Auth Token from twilio.com/console
auth_token  = "db02e938d12c30c3e7f278d118ed7bc3"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+15093080228",
    from_="+12055767590",
    body=message)

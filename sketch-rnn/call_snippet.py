from twilio.rest import Client
"""
This is a notification script which is executed when training is complete.
To use, pls replace with own twilio credentials and number - you can create one for free!
tutorial: https://www.twilio.com/docs/voice/tutorials/how-to-make-outbound-phone-calls-python?code-sample=code-make-an-outbound-call&code-language=Python&code-sdk-version=6.x
"""

account_sid = ''
auth_token = ''
account_phone_number = '' #may need to ocassionally replace, there is a $15 limit for free numbers.

my_phone_number ='' #replace with your phone number

client=Client(account_sid,auth_token)
call = client.calls.create(to=my_phone_number,from_=account_phone_number,url='http://demo.twilio.com/docs/classic.mp3')

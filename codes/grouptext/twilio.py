from django.conf import settings
from twilio.rest import Client
import random


def send_confirmation_code(to_number):
    verification_code = generate_code()
    message_details = twilio_send_sms(to_number, verification_code)
    return verification_code, message_details


def generate_code():
    return str(random.randrange(100000, 999999))


def twilio_send_sms(to_number, body):
    account_sid = settings.TWILIO['TWILIO_ACCOUNT_SID']
    auth_token = settings.TWILIO['TWILIO_AUTH_TOKEN']
    twilio_number = settings.TWILIO['TWILIO_NUMBER']
    client = Client(account_sid, auth_token)
    # sending the sms and response - https://www.twilio.com/docs/sms/quickstart/python
    # This is what we need - this gets the status callback of the message - https://www.twilio.com/docs/sms/tutorials/how-to-confirm-delivery-python
    # message_details = client.api.messages.create(to_number, from_=twilio_number, body=body, status_callback="https://ba0bdb01597f.ngrok.io") # Another argument which is the api callback
    message_details = {"status": "sent", "message_id": "SC4534fd43543r3ryu67"}
    return message_details
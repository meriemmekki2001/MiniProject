import pyotp
import base64
import os
from backend import settings
from twilio.rest import Client

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def generate_otp()->int:
    totp = pyotp.TOTP(base64.b32encode(os.urandom(16)).decode('utf-8'))
    otp = totp.now()
    return otp

def send_sms(message:str, phone:str):
    client.messages.create(
                              body=message,
                              from_=settings.TWILIO_PHONE_NUMBER,
                              to=phone
                          )
    return

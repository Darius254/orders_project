# orders/utils.py

import africastalking
from django.conf import settings

# Initialize Africa's Talking
africastalking.initialize(
    username=settings.AFRICASTALKING_USERNAME,
    api_key=settings.AFRICASTALKING_API_KEY
)

sms = africastalking.SMS

def send_sms_notification(to, message):
    try:
        # to: List of phone numbers (in international format, e.g., +2547XXXXXXXX)
        # message: Text message to send
        response = sms.send(message, [to], sender_id="shortcode_or_sender_id")  # Optional sender ID
        print(f"SMS sent successfully: {response}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

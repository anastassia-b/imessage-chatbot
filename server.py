from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from generator import generate_message

app = Flask(__name__)

# decorator, wraps the function
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()
    ron_message = generate_message(1000)
    resp.message(ron_message)

    return str(resp)

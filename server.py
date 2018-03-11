from flask import Flask, request, redirect, render_template
from flask_cors import CORS
from twilio.twiml.messaging_response import MessagingResponse
# from generator import generate_message
from lstm_generator import generate_message

app = Flask(__name__)
CORS(app)

# decorator, wraps the function
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()
    ron_message = generate_message(459)
    resp.message(ron_message)

    return str(resp)

@app.route("/message", methods=['GET'])
def message_reply():
    return str(generate_message(459))

if __name__ == '__main__':
    app.run()

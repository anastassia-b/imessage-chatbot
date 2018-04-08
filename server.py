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
    resp = MessagingResponse()
    rnn_message = generate_message(450)
    resp.message(rnn_message)

    return str(resp)

@app.route("/message", methods=['GET'])
def message_reply():
    return str(generate_message(250))

if __name__ == '__main__':
    app.run()

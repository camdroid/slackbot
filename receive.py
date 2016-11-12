import os
from flask import Flask, request, Response
from secrets import SLACK_WEBHOOK_SECRET

app = Flask(__name__)

@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')
        inbound_message = username + " in " + channel + " says: " + text
        print(inbound_message)
    return Response('hello!'), 200


@app.route('/', methods=['GET'])
def test():
    return Response('It works!')


if __name__ == "__main__":
    app.run(debug=True)

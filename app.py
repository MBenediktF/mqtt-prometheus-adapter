from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/metrics')
def metrics():
    return "broker_topic_1 12"

app.run(port=4444)
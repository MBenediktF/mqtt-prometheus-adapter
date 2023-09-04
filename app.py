import yaml
config_file_path = './mqtt-prometheus-adapter/config.yml'

from mqtt_client import MQTTClient

import sys

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "MQTT-Prometheus-Adapter is running on this port. <br> Go to the <a href='/metrics'>metrics</a>"

@app.route('/metrics')
def metrics():
    return "broker_topic_1 12"

try:
    with open(config_file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
except FileNotFoundError:
    print("Error: Could not open config file.")
    sys.exit(1)
except yaml.YAMLError as e:
    print(f'Error: Could not read config file: {e}')
    sys.exit(1)

endpoint = config.get('endpoint', False)
if not endpoint:
    print("Error: Endpoint not specified in config")
    sys.exit(1)

port = config.get('endpportoint', False)
if not endpoint:
    print("Error: Port not specified in config")
    sys.exit(1)

print("Endpoint: " + endpoint)
print("Port: " + port)

mqtt = MQTTClient(endpoint, port)
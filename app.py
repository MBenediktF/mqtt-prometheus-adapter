import os
import yaml
config_file_path = os.environ.get('CONFIG_PATH', '/etc/mqtt-prometheus-adapter/config.yml')

from mqtt_client import MQTTClient

import sys

import re

from flask import Flask

try:
    with open(config_file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
except FileNotFoundError:
    print(f"Error: Could not open config file: {config_file_path}")
    sys.exit(1)
except yaml.YAMLError as e:
    print(f'Error: Could not read config file: {e}')
    sys.exit(1)

host = config.get('host', False)
if not host:
    print("Error: Host not specified in config")
    sys.exit(1)

port = config.get('port', False)
if not port:
    print("Error: Port not specified in config")
    sys.exit(1)

topics = config.get('topics', [])

print(str(topics))

print(f'Host: {host}')
print(f'Port: {port}')

mqtt = MQTTClient(host, port, topics)

app = Flask(__name__)
app.run()

@app.route('/')
def index():
    response = "MQTT-Prometheus-Adapter is running on this port.<br>Go to the <a href='/metrics'>metrics</a>"
    return response

@app.route('/metrics')
def metrics():
    data = mqtt.getData()
    response = ""
    for element in data:
        name = next(iter(element))
        if 'conversion' in element and 're_pattern' in element['conversion']:
            try:
                pattern = element['conversion']['re_pattern']
                exports = element['conversion']['exports']
                results = re.findall(pattern, str(element['value']))
                print(f"Results: {results}; Pattern: {pattern}; Value: {element['value']}")
                for index, result in enumerate(results):
                    response += f"{name}_{exports[index]} {result}\n"
            except Exception as e:
                print(f"Error: Could not convert value: {e}")
        elif element['value'] != '':
            response += f"{name} {element['value']}\n"
    return response

#response += f"# HELP {name} {element['path']} "
#response += f"# TYPE {name} {element['type']} "
#response += f"{name} \"{element['value']}\" "
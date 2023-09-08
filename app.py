import os
import yaml
config_file_path = os.environ.get('CONFIG_PATH', '/etc/mqtt-prometheus-adapter/config.yml')

from mqtt_client import MQTTClient

import sys

from prometheus_client import start_http_server, Gauge

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

for topic in topics:
    name = str(next(iter(topic)))
    if 'conversion' in topic and 're_pattern' in topic['conversion']:
        try:
            exports = topic['conversion']['exports']
            child_name = topic['conversion']['child_name']
            topic.update({'prometheus_object': Gauge(next(iter(topic)), str(topic['description']), ['child'])})
        except Exception as e:
            print(f"Error: Could not convert value: {e}")
    else:
        topic.update({'prometheus_object': Gauge(next(iter(topic)), str(topic['description']))})

start_http_server(4444)

mqtt = MQTTClient(host, port, topics)
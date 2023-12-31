import os
import yaml
config_file_path = os.environ.get('CONFIG_PATH', '/etc/mqtt-prometheus-adapter/config.yml')

from mqtt_client import MQTTClient

import sys

from prometheus_client import start_http_server, Gauge, Counter

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

log_topic_updates = config.get('log_topic_updates', False)

topics = config.get('topics', [])

polling = config.get('polling', {})
polling_interval = polling.get('interval', 15)
polling_topics = polling.get('topics', False)

if isinstance(polling_topics, list) == False:
    print("Could not read polling topics: Please check the configuration.")
    polling_topics = False

for topic in topics:
    name = str(next(iter(topic)))
    type = topic.get('type', "gauge")
    if 'conversion' in topic and 're_pattern' in topic['conversion'] and type == "gauge":
        try:
            exports = topic['conversion']['exports']
            topic.update({'prometheus_object': Gauge(name, str(topic['description']), ['child'])})
        except Exception as e:
            print(f"Error: Could not convert value: {e}")
    elif type == "counter":
        topic.update({'prometheus_object': Counter(name, str(topic['description']))})
    elif type == "gauge":
        topic.update({'prometheus_object': Gauge(name, str(topic['description']))})
    else: 
        print(f"Error: Unknown type for topic {name}: {type}")

start_http_server(4444)

mqtt = MQTTClient(host, port, topics, polling_interval, polling_topics, log_topic_updates)
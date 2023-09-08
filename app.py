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

print(str(topics))

print(f'Host: {host}')
print(f'Port: {port}')

for topic in topics:
    name = str(next(iter(topic)))
    print(name)
    if 'conversion' in topic and 're_pattern' in topic['conversion']:
        try:
            exports = topic['conversion']['exports']
            child_name = topic['conversion']['child_name']
            for index, export in enumerate(exports):
                topic.update({'prometheus_object': Gauge(next(iter(topic)), "Topic description", [str(child_name)])})
        except Exception as e:
            print(f"Error: Could not convert value: {e}")
    else:
        topic.update({'prometheus_object': Gauge(next(iter(topic)), "Topic description")})
    
start_http_server(4444)

mqtt = MQTTClient(host, port, topics)


#response += f"# HELP {name} {element['path']} "
#response += f"# TYPE {name} {element['type']} "
#response += f"{name} \"{element['value']}\" "
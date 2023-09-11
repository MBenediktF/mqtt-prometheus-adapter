import paho.mqtt.client as mqtt
import sys
import threading
import re

class MQTTClient:
    def __init__(self, host, port, topics, log_topic_updates):
        self.topics = topics
        self.log_topic_updates = log_topic_updates
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
    
        # Connect to host
        try:
            client.connect(host, port)
        except Exception as e:
            print(f"Error connecting to host: {e}")
            sys.exit(1)

        mqtt_loop_thread = threading.Thread(target=client.loop_forever)
        mqtt_loop_thread.start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        for topic in self.topics:
            client.subscribe(topic['path'])
            print(f"Subscribed to topic: {topic['path']}")

    def on_message(self, client, userdata, msg):
        if self.log_topic_updates:
            print(f"Received topic update: {msg.topic} : {msg.value}")
        # Set new value
        for topic in self.topics:
            if topic['path'] == msg.topic:
                self.set_prometheus_payload(topic, msg.payload)
                break

    def set_prometheus_payload(self, topic, payload):
        if 'conversion' in topic and 're_pattern' in topic['conversion']:
            try:
                pattern = topic['conversion']['re_pattern']
                exports = topic['conversion']['exports']
                results = re.findall(pattern, str(payload))
                for index, result in enumerate(results):
                    prometheus_object = topic['prometheus_object']
                    prometheus_object.labels(child=str(exports[index])).set(result)
            except Exception as e:
                print(f"Error: Could not convert incomming payload {payload} on topic {topic}: {e}")
        else:
            try:
                topic['prometheus_object'].set(payload)
            except Exception as e:
                print(f"Error: Could not write incomming payload {payload} on topic {topic}: {e}")

        

    def getData(self):
        return self.topics
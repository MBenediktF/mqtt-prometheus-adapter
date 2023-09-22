import paho.mqtt.client as mqtt
import sys
import threading
import re
import time

class MQTTClient:
    def __init__(self, host, port, topics, polling_interval, polling_topics, log_topic_updates):
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

        if polling_topics != False:
            print("Starting polling")
            polling_thread = threading.Thread(target=self.periodic_publish, args=(client, polling_interval, polling_topics))
            polling_thread.start()
        

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        for topic in self.topics:
            client.subscribe(topic['path'])
            print(f"Subscribed to topic: {topic['path']}")

    def on_message(self, client, userdata, msg):
        if self.log_topic_updates:
            print(f"Received topic update: {msg.topic} : {msg.payload}")
        # Set new value
        for topic in self.topics:
            if topic['path'] == msg.topic:
                self.set_prometheus_payload(topic, msg.payload)
                break

    def set_prometheus_payload(self, topic, payload):
        type = topic.get('type', "gauge")
        if 'conversion' in topic and 're_pattern' in topic['conversion'] and type == "gauge":
            try:
                pattern = topic['conversion']['re_pattern']
                exports = topic['conversion']['exports']
                prometheus_object = topic['prometheus_object']
                results = re.findall(pattern, str(payload))
                for index, result in enumerate(results):
                    if len(exports)-1 < index: break
                    export = exports[index]
                    export_name = export
                    mapping = False
                    if isinstance(export, dict):
                        mapping = export.get('mapping', False)
                    if mapping:
                        export_name = str(next(iter(export)))
                        result = mapping.get(result, False)
                        if result == False:
                            print(f"Warning: Could not map converted payload: {results[index]}")
                            continue
                    prometheus_object.labels(child=str(export_name)).set(result)   
            except Exception as e:
                print(f"Error: Could not convert incomming payload {payload} on topic {topic['path']}: {e}")
        elif type == "counter":
            try:
                filter = topic.get('filter', False)
                if filter and re.search(filter, str(payload)) == None:
                    return
                topic['prometheus_object'].inc()
            except Exception as e:
                print(f"Error: Could not filter incomming payload {payload} on topic {topic['path']}: {e}")
        elif type == "gauge":
            try:
                topic['prometheus_object'].set(payload)
            except Exception as e:
                print(f"Error: Could not write incomming payload {payload} on topic {topic['path']}: {e}")
        else:
            print(f"Warning: Skipping received message on topic {topic['path']} for reason: Unknown type")

    def periodic_publish(client, interval, topics):
        while(True):
            try:
                for key, value in topics.items():
                    print(f"Topic to publish: {key}, Value: {value}")
                    client.publish(key, value)
            except Exception as e:
                print(f"Error initiating polling: {e}")
                sys.exit(1)
            time.sleep(interval)
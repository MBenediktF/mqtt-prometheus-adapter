import paho.mqtt.client as mqtt
import sys

class MQTTClient:
    def __init__(self, host, port, topics):
        self.topics = topics
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
    
        # Connect to host
        try:
            client.connect(host, port)
        except Exception as e:
            print(f"Error connecting to host: {e}")
            sys.exit(1)

        client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        for topic in self.topics:
            client.subscribe(topic['path'])
            print(f"Subscribed to topic: {topic['path']}")

            # Add value field
            topic.update({'value':''})

    def on_message(self, client, userdata, msg):
        print(f"Received message on {msg.topic} with payload {msg.payload}")

        # Set new value
        for topic in self.topics:
            if topic['path'] == msg.topic:
                topic['value'] = msg.payload


    def getData():
        return []
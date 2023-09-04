import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, host, port, topics):
        self.topics = topics
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(host, port)
        print("Test")
        client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        for topic in self.topics:
            print(topic.path)
            client.subscribe(topic.path)

    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    def getData():
        return []
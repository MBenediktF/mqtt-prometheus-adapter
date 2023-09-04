import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, endpoint, port):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(endpoint, port, 60)

        client.loop_forever()

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        client.subscribe("")

    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
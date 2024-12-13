import argparse
import paho.mqtt.client as mqtt

def parse_args():
    parser = argparse.ArgumentParser(description='MQTT to InfluxDB bridge.')
    parser.add_argument('--url', type=str, default='http://localhost:8086', help='InfluxDB URL')
    parser.add_argument('--bucket', type=str, default='iot', help='InfluxDB bucket name')
    parser.add_argument('--mqtt-broker', type=str, default='localhost', help='MQTT broker address')
    parser.add_argument('--mqtt-topic', type=str, default='sensors', help='MQTT topic to subscribe')
    return parser.parse_args()

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode('utf-8')} on topic: {msg.topic}")

def main(mqtt_broker, mqtt_topic):
    mqtt_client = mqtt.Client()
    mqtt_client.on_message = on_message

    print(f"Connecting to MQTT broker {mqtt_broker}...")
    mqtt_client.connect(mqtt_broker)

    print(f"Subscribing to topic {mqtt_topic}...")
    mqtt_client.subscribe(mqtt_topic)

    mqtt_client.loop_forever()

if __name__ == "__main__":
    args = parse_args()
    main(args.mqtt_broker, args.mqtt_topic)
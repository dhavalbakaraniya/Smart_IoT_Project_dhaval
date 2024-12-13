import argparse
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

def parse_args():
    parser = argparse.ArgumentParser(description='MQTT to InfluxDB bridge.')
    parser.add_argument('--url', type=str, default='http://localhost:8086', help='InfluxDB URL')
    parser.add_argument('--bucket', type=str, default='iot', help='InfluxDB bucket name')
    parser.add_argument('--mqtt-broker', type=str, default='localhost', help='MQTT broker address')
    parser.add_argument('--mqtt-topic', type=str, default='sensors', help='MQTT topic to subscribe')
    return parser.parse_args()

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode('utf-8')} on topic: {msg.topic}")
    
    # Prepare the data point for InfluxDB
    payload = float(msg.payload.decode('utf-8'))
    point = Point("sensor_data").field("value", payload)

    # Write data to InfluxDB
    write_api = userdata['write_api']
    write_api.write(bucket=userdata['bucket'], record=point)
    print("Data written to InfluxDB.")

def main(url, bucket, mqtt_broker, mqtt_topic):
    # Setup InfluxDB client
    client = InfluxDBClient(url=url)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    mqtt_client = mqtt.Client(userdata={"write_api": write_api, "bucket": bucket})
    mqtt_client.on_message = on_message

    print(f"Connecting to MQTT broker {mqtt_broker}...")
    mqtt_client.connect(mqtt_broker)

    print(f"Subscribing to topic {mqtt_topic}...")
    mqtt_client.subscribe(mqtt_topic)

    mqtt_client.loop_forever()

if __name__ == "__main__":
    args = parse_args()
    main(args.url, args.bucket, args.mqtt_broker, args.mqtt_topic)
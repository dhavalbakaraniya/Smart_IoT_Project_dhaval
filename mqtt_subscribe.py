import argparse
import logging
import os
import signal
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Configure logging
logging.basicConfig(level=logging.INFO)

def parse_args():
    parser = argparse.ArgumentParser(description='MQTT to InfluxDB bridge.')
    parser.add_argument('--url', type=str, default=os.getenv('INFLUXDB_URL', 'http://localhost:8086'), help='InfluxDB URL')
    parser.add_argument('--bucket', type=str, default=os.getenv('INFLUXDB_BUCKET', 'iot'), help='InfluxDB bucket name')
    parser.add_argument('--mqtt-broker', type=str, default=os.getenv('MQTT_BROKER', 'localhost'), help='MQTT broker address')
    parser.add_argument('--mqtt-topic', type=str, default=os.getenv('MQTT_TOPIC', 'sensors'), help='MQTT topic to subscribe')
    return parser.parse_args()

def on_message(client, userdata, msg):
    try:
        logging.info(f"Received message: {msg.payload.decode('utf-8')} on topic: {msg.topic}")

        # Filter messages for specific criteria (for example, topic-based filtering)
        if msg.topic != userdata['expected_topic']:
            logging.info(f"Ignored message from topic: {msg.topic}")
            return
        
        # Prepare the data point for InfluxDB
        payload = float(msg.payload.decode('utf-8'))
        point = Point("sensor_data").field("value", payload)

        # Write data to InfluxDB
        write_api = userdata['write_api']
        write_api.write(bucket=userdata['bucket'], record=point)
        logging.info("Data written to InfluxDB.")
    except Exception as e:
        logging.error(f"Error processing message: {e}")

def main(url, bucket, mqtt_broker, mqtt_topic):
    client = InfluxDBClient(url=url)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    mqtt_client = mqtt.Client(userdata={"write_api": write_api, "bucket": bucket, "expected_topic": mqtt_topic})
    mqtt_client.on_message = on_message

    def signal_handler(sig, frame):
        logging.info('Gracefully shutting down...')
        mqtt_client.disconnect()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logging.info(f"Connecting to MQTT broker {mqtt_broker}...")
    mqtt_client.connect(mqtt_broker)

    logging.info(f"Subscribing to topic {mqtt_topic}...")
    mqtt_client.subscribe(mqtt_topic)

    mqtt_client.loop_forever()

if __name__ == "__main__":
    args = parse_args()
    main(args.url, args.bucket, args.mqtt_broker, args.mqtt_topic)
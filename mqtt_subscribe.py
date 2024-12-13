import argparse
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Callback function when a message is received from the MQTT broker
def on_message(client, userdata, msg):
    try:
        # Decode the payload and log it
        payload = msg.payload.decode('utf-8')
        print(f"Received message on topic {msg.topic}: {payload}")

        # Parse the payload (assuming it's a simple value; adjust if JSON or other format)
        humidity_value = float(payload)

        # Create a data point
        point = Point("sensor1") \
            .field("measuring", humidity_value) \
            .tag("type", "moisture")

        # Write to InfluxDB
        userdata['write_api'].write(bucket=userdata['bucket'], record=point)
        print("Data written to InfluxDB successfully.")

        # Increment the message count
        userdata['message_count'] += 1
        if userdata['message_count'] >= userdata['max_messages']:
            print("Processed the maximum number of messages. Stopping.")
            client.disconnect()  # Disconnect the MQTT client
    except Exception as e:
        print(f"Error processing message: {e}")

def main(url, org, bucket, token, mqtt_broker, mqtt_port, mqtt_topic, max_messages):
    # Create the InfluxDB client
    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    # Configure MQTT client
    mqtt_client = mqtt.Client(userdata={"write_api": write_api, "bucket": bucket, "message_count": 0, "max_messages": max_messages})
    mqtt_client.on_message = on_message

    # Connect to the MQTT broker
    print(f"Connecting to MQTT broker {mqtt_broker}:{mqtt_port}...")
    mqtt_client.connect(mqtt_broker, mqtt_port, 60)

    # Subscribe to the MQTT topic
    print(f"Subscribing to topic {mqtt_topic}...")
    mqtt_client.subscribe(mqtt_topic)

    # Start MQTT loop (blocks until stopped)
    mqtt_client.loop_forever()

    # Cleanup
    client.close()
    print("InfluxDB client closed.")

def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(description='MQTT to InfluxDB bridge.')
    parser.add_argument('--url', type=str, required=False,
                        default='https://us-east-1-1.aws.cloud2.influxdata.com',
                        help='InfluxDB hostname INCLUDING port for local installations')
    parser.add_argument('--bucket', type=str, required=False, default='smart-iot',
                        help='InfluxDB bucket to use for writing data')
    parser.add_argument('--org', type=str, required=False, default='smart-iot',
                        help='Organization name as configured in InfluxDB UI')
    parser.add_argument('--token', type=str, required=False,
                        default='11jFHQgTnbF7zT3aqHiAbMVMMnBR_E0W3alzu4lSYU_a-prnLLL8Ey7YnQNkfVNCG6hH59f0DbB82Eum-lot5w==',
                        help='InfluxDB API token generated in the InfluxDB UI')
    parser.add_argument('--mqtt-broker', type=str, required=False,
                        default='test.mosquitto.org',
                        help='MQTT broker hostname or IP address')
    parser.add_argument('--mqtt-port', type=int, required=False, default=1883,
                        help='MQTT broker port')
    parser.add_argument('--mqtt-topic', type=str, required=False, default='dar_val',
                        help='MQTT topic to subscribe to')
    parser.add_argument('--max-messages', type=int, required=False, default=25,
                        help='Number of messages to process before stopping')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(url=args.url, org=args.org, bucket=args.bucket, token=args.token,
         mqtt_broker=args.mqtt_broker, mqtt_port=args.mqtt_port, mqtt_topic=args.mqtt_topic, max_messages=args.max_messages)

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='MQTT to InfluxDB bridge.')
    parser.add_argument('--url', type=str, default='http://localhost:8086', help='InfluxDB URL')
    parser.add_argument('--bucket', type=str, default='iot', help='InfluxDB bucket name')
    parser.add_argument('--mqtt-broker', type=str, default='localhost', help='MQTT broker address')
    parser.add_argument('--mqtt-topic', type=str, default='sensors', help='MQTT topic to subscribe')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    print(f"Parsed arguments: {args}")
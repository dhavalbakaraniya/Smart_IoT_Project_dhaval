from fastapi import FastAPI
import paho.mqtt.client as mqtt
import threading

app = FastAPI()

# Global variable to store the latest moisture value
latest_moisture_value = "No Data Yet"

# MQTT Setup
BROKER = "test.mosquitto.org"
TOPIC = "dar_val"

def on_message(client, userdata, message):
    global latest_moisture_value
    latest_moisture_value = message.payload.decode()

def mqtt_subscribe():
    client = mqtt.Client()
    client.on_message = on_message
   

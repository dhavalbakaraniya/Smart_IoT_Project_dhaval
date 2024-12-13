from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import paho.mqtt.client as mqtt
import threading
from datetime import datetime

app = FastAPI()

# Global variable to store the latest moisture value
latest_moisture_value = "No Data Yet"

# Log list to store entries of low humidity detections
low_humidity_log = []

# MQTT Setup
BROKER = "test.mosquitto.org"
TOPIC = "dar_val"

def on_message(client, userdata, message):
    """Callback for MQTT message reception"""
    global latest_moisture_value
    latest_moisture_value = message.payload.decode()

    # Check if moisture value is low and log the event
    if float(latest_moisture_value) <= 300:
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "moisture_value": latest_moisture_value
        }
        low_humidity_log.append(log_entry)

def mqtt_subscribe():
    """Subscribe to MQTT topic in a separate thread"""
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)
    client.subscribe(TOPIC)
    client.loop_forever()

# Start MQTT in a separate thread
mqtt_thread = threading.Thread(target=mqtt_subscribe)
mqtt_thread.daemon = True
mqtt_thread.start()

@app.get("/humidity")
def read_humidity():
    """Endpoint to retrieve the latest moisture value"""
    return {"moisture_value": latest_moisture_value}

@app.get("/low_humidity_log")
def get_low_humidity_log():
    """Endpoint to retrieve the log of low humidity detections"""
    return {"low_humidity_log": low_humidity_log}

# Serve the index.html file
@app.get("/", response_class=HTMLResponse)
def get_index():
    """Serve the main HTML page"""
    with open("templates/index.html", "r") as file:
        return HTMLResponse(content=file.read())

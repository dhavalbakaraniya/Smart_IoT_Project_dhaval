import asyncio
import threading
import requests
import paho.mqtt.client as mqtt
from telegram import Bot

# Configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "dar_val"
TELEGRAM_TOKEN = "7383173396:AAFWK3sSGfNM8TaIGce7-L17bg8HTF4glb0"
TELEGRAM_CHAT_ID = None  # Dynamically fetched later

flag = 0  # Alert flag to prevent repeated messages

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_TOKEN)

# Create a persistent event loop
event_loop = asyncio.new_event_loop()
asyncio.set_event_loop(event_loop)

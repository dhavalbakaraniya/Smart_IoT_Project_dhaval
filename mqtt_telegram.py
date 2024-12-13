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

# Function to dynamically fetch the chat ID
def get_chat_id():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["ok"] and "result" in data and len(data["result"]) > 0:
            chat_id = data["result"][-1]["message"]["chat"]["id"]
            print(f"Chat ID fetched successfully: {chat_id}")
            return chat_id
        else:
            print("No chat updates found. Please send a message to your bot first.")
            return None
    except Exception as e:
        print(f"Error fetching chat ID: {e}")
        return None

# Fetch the Telegram chat ID
TELEGRAM_CHAT_ID = get_chat_id()
if TELEGRAM_CHAT_ID is None:
    print("Failed to fetch Telegram chat ID. Exiting...")
    exit(1)
# Asynchronous function to send a Telegram message
async def send_telegram_message(message):
    try:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print("Notification sent to Telegram.")
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

# Wrapper function to schedule tasks in the event loop
def schedule_task(coro):
    asyncio.run_coroutine_threadsafe(coro, event_loop)


# Create a persistent event loop
event_loop = asyncio.new_event_loop()
asyncio.set_event_loop(event_loop)

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

flag = 0

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_TOKEN)

# Create a persistent event loop
event_loop = asyncio.new_event_loop()
asyncio.set_event_loop(event_loop)

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

# MQTT Callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        global flag
        # Parse the message payload
        humidity = float(msg.payload.decode())
        print(f"Received Humidity: {humidity}")

        # Check humidity threshold and send a notification
        if humidity < 300:
            if flag == 0:
                
                flag = 1
                message = f"Alert! Low humidity detected"
                schedule_task(send_telegram_message(message))
            
            else:
                flag = 0  # Example threshold
            # if flag is 0:
                  # Schedule the async function
                # flag = 1
        # else:
        #     flag = 0
    except Exception as e:
        print(f"Error processing message: {e}")

# MQTT Client Setup
client = mqtt.Client(protocol=mqtt.MQTTv311)  # Use explicit protocol version
client.on_connect = on_connect
client.on_message = on_message

# Start the event loop in a background thread
loop_thread = threading.Thread(target=event_loop.run_forever, daemon=True)
loop_thread.start()

# Connect to the MQTT broker and start listening
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()

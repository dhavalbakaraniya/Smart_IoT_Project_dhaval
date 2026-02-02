# Smart IoT - Automatic Plant Watering System

A Smart IoT project for **automatic plant watering** using M5Stack with soil moisture sensor, MQTT protocol, real-time dashboard, InfluxDB time-series database, and Telegram bot notifications.

---

## Developer

| Name | Email |
|------|-------|
| **Dhaval Bakaraniya** | dhavalbakaraniya31@gmail.com |

---

## Project Information

| Field | Details |
|-------|---------|
| **Project** | Automatic Watering System for Plants |
| **Course** | Smart IoT |
| **Semester** | Winter Semester 2024/2025 |
| **University** | Ostfalia University of Applied Sciences |
| **Group** | Gruppe 014 |

---

## Abstract

This project implements an automatic plant watering system using IoT technology. A soil moisture sensor connected to an M5Stack device continuously monitors soil humidity levels. When the moisture drops below a threshold (300), the system:

- Sends **Telegram alerts** to notify the user
- Logs data to **InfluxDB** for historical analysis
- Displays real-time values on a **web dashboard**
- Changes the M5Stack screen color (red = dry, green = normal)

---

## Features

### Hardware Features
- **M5Stack Core** - Main IoT controller with display
- **Soil Moisture Sensor (EARTH Unit)** - Analog moisture detection
- **Real-time Display** - Shows moisture value with color-coded status

### Software Features
- **MQTT Communication** - Publish/subscribe messaging via Mosquitto
- **FastAPI Dashboard** - Real-time web interface for monitoring
- **InfluxDB Integration** - Time-series data storage for analytics
- **Telegram Bot Alerts** - Instant notifications when soil is dry
- **Low Humidity Logging** - Historical log of dry conditions

### Monitoring Capabilities
- Live moisture value display
- Color-coded status (Green = Normal, Red = Dry)
- Timestamp-based humidity logs
- Historical data visualization via InfluxDB

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| **IoT Device** | M5Stack Core |
| **Sensor** | EARTH Unit (Soil Moisture) |
| **Programming** | Python, MicroPython (UIFlow) |
| **Message Broker** | MQTT (test.mosquitto.org) |
| **Web Framework** | FastAPI |
| **Database** | InfluxDB Cloud |
| **Notifications** | Telegram Bot API |
| **Frontend** | HTML, CSS, JavaScript |

---

## Project Structure

```
Smart_IoT_Project/
├── fastapi_server.py              # FastAPI web server with dashboard
├── mqtt_subscribe.py              # MQTT to InfluxDB bridge
├── mqtt_telegram.py               # MQTT to Telegram notification service
├── ui_flow_humidity_sensor.py     # M5Stack MicroPython code
├── ui_flow_humidity_sensor.m5f    # UIFlow project file
├── template/
│   └── index.html                 # Real-time monitoring dashboard
└── doc/
    ├── Automatic Watering System For Plants-1.pdf
    ├── dashboard.jpeg             # Dashboard screenshot
    ├── telegram message.jpeg      # Telegram notification example
    └── group014.jpg               # Team photo
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Smart IoT System                              │
│                                                                      │
│  ┌──────────────┐         ┌──────────────────┐                      │
│  │   M5Stack    │  MQTT   │    Mosquitto     │                      │
│  │ + Soil Sensor│────────▶│    Broker        │                      │
│  └──────────────┘         └──────────────────┘                      │
│                                   │                                  │
│           ┌───────────────────────┼───────────────────────┐         │
│           │                       │                       │         │
│           ▼                       ▼                       ▼         │
│  ┌──────────────┐       ┌──────────────┐       ┌──────────────┐    │
│  │   FastAPI    │       │  InfluxDB    │       │   Telegram   │    │
│  │  Dashboard   │       │   Storage    │       │     Bot      │    │
│  └──────────────┘       └──────────────┘       └──────────────┘    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Getting Started

### Prerequisites

- **Python 3.8+**
- **M5Stack Core** with EARTH (Soil Moisture) Unit
- **pip** (Python package manager)
- **Telegram Account** (for bot notifications)
- **InfluxDB Cloud Account** (for data storage)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dhavalbakaraniya/Smart_IoT_Project_dhaval.git
   cd Smart_IoT_Project_dhaval
   ```

2. **Install Python dependencies**
   ```bash
   pip install fastapi uvicorn paho-mqtt influxdb-client python-telegram-bot requests
   ```

3. **Configure M5Stack**
   - Open UIFlow (https://flow.m5stack.com/)
   - Load `ui_flow_humidity_sensor.m5f`
   - Connect your M5Stack and upload the code

---

## Running the Application

### 1. Start the FastAPI Dashboard

```bash
uvicorn fastapi_server:app --host 0.0.0.0 --port 8000 --reload
```

Access the dashboard at: `http://localhost:8000`

### 2. Start the MQTT to InfluxDB Bridge

```bash
python mqtt_subscribe.py
```

**Command line options:**
```bash
python mqtt_subscribe.py --help

Options:
  --url           InfluxDB URL (default: InfluxDB Cloud)
  --bucket        InfluxDB bucket name (default: smart-iot)
  --org           InfluxDB organization (default: smart-iot)
  --token         InfluxDB API token
  --mqtt-broker   MQTT broker address (default: test.mosquitto.org)
  --mqtt-port     MQTT broker port (default: 1883)
  --mqtt-topic    MQTT topic to subscribe (default: dar_val)
  --max-messages  Number of messages to process (default: 25)
```

### 3. Start the Telegram Notification Service

```bash
python mqtt_telegram.py
```

> **Note:** You need to send a message to your Telegram bot first to get the chat ID.

---

## Configuration

### MQTT Settings

| Parameter | Default Value |
|-----------|---------------|
| Broker | test.mosquitto.org |
| Port | 1883 |
| Topic | dar_val |

### InfluxDB Settings

| Parameter | Default Value |
|-----------|---------------|
| URL | https://us-east-1-1.aws.cloud2.influxdata.com |
| Bucket | smart-iot |
| Organization | smart-iot |

### Moisture Threshold

| Value | Status |
|-------|--------|
| ≤ 300 | Dry (Alert triggered) |
| > 300 | Normal |

---

## M5Stack Setup

### Hardware Connection

1. Connect the **EARTH Unit** to **Port B** on M5Stack
2. Power on the M5Stack

### UIFlow Programming

The M5Stack code (`ui_flow_humidity_sensor.py`) does the following:

1. Reads analog moisture value from sensor
2. Publishes value to MQTT topic `dar_val`
3. Updates screen display with current value
4. Changes background color:
   - **Red** (0xff0000) - Moisture ≤ 300 (Dry)
   - **Green** (0x33ff33) - Moisture > 300 (Normal)

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard page |
| `/humidity` | GET | Get latest moisture value |
| `/low_humidity_log` | GET | Get log of low humidity events |

### Example Response

**GET /humidity**
```json
{
  "moisture_value": "450"
}
```

**GET /low_humidity_log**
```json
{
  "low_humidity_log": [
    {
      "timestamp": "2024-12-15 14:30:22",
      "moisture_value": "285"
    }
  ]
}
```

---

## Dashboard Features

The web dashboard (`template/index.html`) provides:

- **Real-time Moisture Display** - Updates every 2 seconds
- **Status Indicator** - Shows "Soil is Dry" or "Moisture is Normal"
- **Low Humidity Log Table** - Historical record of dry events
- **Animated UI** - Pulse animation and hover effects
- **Responsive Design** - Works on desktop and mobile

---

## Telegram Bot Setup

1. Create a new bot via [@BotFather](https://t.me/BotFather) on Telegram
2. Get your bot token
3. Send any message to your bot
4. Update the `TELEGRAM_TOKEN` in `mqtt_telegram.py`
5. Run the script - it will automatically fetch your chat ID

**Alert Message Example:**
```
Alert! Low humidity detected
```

---

## Data Flow

```
1. Sensor reads moisture value
         ↓
2. M5Stack publishes to MQTT topic "dar_val"
         ↓
3. Three subscribers receive the data:
   ├── FastAPI Server → Updates dashboard
   ├── InfluxDB Bridge → Stores in database
   └── Telegram Bot → Sends alert if low
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **M5Stack not sending data** | Check WiFi connection and MQTT broker |
| **Dashboard shows "Loading..."** | Verify FastAPI server is running |
| **Telegram not receiving alerts** | Send a message to bot first to get chat ID |
| **InfluxDB write fails** | Check API token and bucket permissions |
| **MQTT connection refused** | Verify broker address and port |

---

## Screenshots

### Dashboard
See `doc/dashboard.jpeg` for the web dashboard interface.

### Telegram Notification
See `doc/telegram message.jpeg` for notification example.

---

## Future Improvements

- [ ] Automatic water pump control
- [ ] Multiple sensor support
- [ ] Mobile app integration
- [ ] Weather API integration
- [ ] Historical data charts
- [ ] Configurable alert thresholds

---

## References

- [M5Stack Documentation](https://docs.m5stack.com/)
- [UIFlow Documentation](https://docs.m5stack.com/en/quick_start/core2/uiflow)
- [Paho MQTT Python](https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [InfluxDB Documentation](https://docs.influxdata.com/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

## License

This project is developed for educational purposes at Ostfalia University of Applied Sciences.

---

*Last Updated: February 2026*

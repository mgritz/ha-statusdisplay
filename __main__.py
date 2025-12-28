
import paho.mqtt.client as mqtt
import time
import signal

from display import DisplayUpdater

try:
    from credentials import MQTT_USER, MQTT_PW, MQTT_BROKER, MQTT_PORT
except ImportError:
    MQTT_USER = None
    MQTT_PW = None
    MQTT_BROKER = "localhost"
    MQTT_PORT = 1883

# MQTT broker settings
TOPIC = "#"  # Subscribe to all topics

def main():
    display_updater = DisplayUpdater()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if MQTT_USER and MQTT_PW:
        client.username_pw_set(MQTT_USER, MQTT_PW)

    def on_connect(client, _userdata, _flags, rc, _properties):
        print(f"Connected with result code {rc}")
        client.subscribe(TOPIC)

    def on_message(_client, _userdata, msg):
        topic_text = msg.topic.replace("window/binary_sensor.","")
        topic_text = topic_text.replace("sensor", "").replace("_offnung","")
        topic_text = topic_text.replace("/state","").title()

        message_value = msg.payload.decode().lower() != "off"
        display_updater.notify(topic_text, message_value)

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("Subscribed to all topics. Listening for messages...")
    running = True

    def handle_sigterm(_signum, _frame):
        nonlocal running
        print("Received SIGTERM, shutting down...")
        running = False

    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGINT, handle_sigterm)  # Also handle Ctrl+C

    display_updater.start()
    client.loop_start()
    try:
        while running:
            time.sleep(1)
    finally:
        client.loop_stop()
        client.disconnect()
        display_updater.stop()

if __name__ == "__main__":
    main()

"""
uart_to_mqtt.py — Script per a la Raspberry que llegeix el gateway LoRa (UART)
i publica les dades al broker MQTT.

Execució: python uart_to_mqtt.py
"""

import json
import serial
import paho.mqtt.client as mqtt

# Configuració
SERIAL_PORT = "/dev/ttyUSB0"   # Port USB on connectes el gateway
BAUDRATE = 115200
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "hort/sensors"


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"✅ Connectat al broker MQTT {MQTT_BROKER}:{MQTT_PORT}")
    else:
        print(f"❌ Error MQTT: rc={rc}")


def main():
    # MQTT
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()

    # Serial
    print(f"📡 Obrint port {SERIAL_PORT} a {BAUDRATE} baud...")
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    print("✅ Port obert, escoltant dades del gateway LoRa...")

    buffer = ""
    while True:
        try:
            data = ser.read(1).decode("utf-8", errors="ignore")
            if not data:
                continue

            if data == "\n":
                line = buffer.strip()
                buffer = ""
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                    sensor_type = payload.get("type", "unknown")
                    sensor_id = payload.get("sensor_id", "unknown")
                    topic = f"{MQTT_TOPIC}/{sensor_type}/{sensor_id}"
                    mqtt_client.publish(topic, json.dumps(payload))
                    print(f"📤 MQTT → {topic}: {payload}")
                except json.JSONDecodeError:
                    print(f"⚠️  Línia no JSON: {line}")
            else:
                buffer += data
        except KeyboardInterrupt:
            print("\n👋 Tancant...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()

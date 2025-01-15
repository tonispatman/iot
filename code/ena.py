import requests
import time
import hmac
import hashlib
import base64
import json
from datetime import datetime
from awscrt import mqtt
from awsiot import mqtt_connection_builder
import threading

# SwitchBot API credentials
API_TOKEN = 'f09df5b1cf220104c6e601bcb932c69ab1cf72f51dd9153c4ddc1dbb33fc567192b907a570c7027e95f59f1c3b8378f1'
SECRET_KEY = '31f4bfcfb7c1cd834f5a40f82b1cf29c'

def generate_headers():
    timestamp = int(round(time.time() * 1000))
    nonce = ''
    string_to_sign = f"{API_TOKEN}{timestamp}{nonce}"
    sign = base64.b64encode(
        hmac.new(SECRET_KEY.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha256).digest()
    ).decode('utf-8')

    return {
        'Authorization': API_TOKEN, 
        'sign': sign,
        't': str(timestamp),
        'nonce': nonce,
        'Content-Type': 'application/json; charset=utf8',
    }

def get_device_status(device_id):
    url = f'https://api.switch-bot.com/v1.1/devices/{device_id}/status'
    headers = generate_headers()
    response = requests.get(url, headers=headers)
    return response.json()

# AWS IoT credentials
AWS_ENDPOINT = "a1nzfuf7k42zd6-ats.iot.us-east-1.amazonaws.com"  # Replace with your endpoint
CA_FILE = "root-CA.crt"
CERT_FILE = "enas.cert.pem"
KEY_FILE = "enas.private.key"
CLIENT_ID = "basicPubSub"
TOPIC = "sdk/test/python"

# MQTT setup
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=AWS_ENDPOINT,
    cert_filepath=CERT_FILE,
    pri_key_filepath=KEY_FILE,
    ca_filepath=CA_FILE,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30
)

# MQTT connect
print(f"Connecting to {AWS_ENDPOINT} with client ID '{CLIENT_ID}'...")
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")

def monitor_and_publish(device_id, interval=60):
    print(f"Starting monitoring for device ID: {device_id}")
    while True:
        try:
            status = get_device_status(device_id)
            if status['statusCode'] == 100:
                body = status['body']
                temperature = body.get('temperature')
                humidity = body.get('humidity')
                battery = body.get('battery')
                received_timestamp = datetime.utcnow().isoformat() + "Z"  # UTC time in ISO 8601 format
                
                data = {
                    "temperature": temperature,
                    "humidity": humidity,
                    "battery": battery,
                    "received_timestamp": received_timestamp
                }
                print(f"Publishing to topic '{TOPIC}': {data}")
                mqtt_connection.publish(
                    topic=TOPIC,
                    payload=json.dumps(data),
                    qos=mqtt.QoS.AT_LEAST_ONCE
                )
            else:
                print("Failed to fetch status:", status)
        except Exception as e:
            print("Error while monitoring and publishing:", e)

        time.sleep(interval)

if __name__ == '__main__':
    DEVICE_ID = 'D5303835164E'  # Replace with your device ID
    try:
        monitor_and_publish(DEVICE_ID, interval=60)
    finally:
        print("Disconnecting...")
        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()
        print("Disconnected!")

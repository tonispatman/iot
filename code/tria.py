import requests
import time
import hmac
import hashlib
import base64

# Replace with your API token and secret key from the SwitchBot app
API_TOKEN = 'f09df5b1cf220104c6e601bcb932c69ab1cf72f51dd9153c4ddc1dbb33fc567192b907a570c7027e95f59f1c3b8378f1'
SECRET_KEY = '31f4bfcfb7c1cd834f5a40f82b1cf29c'

# Generate the authentication headers for SwitchBot API
def generate_headers():
    timestamp = int(round(time.time() * 1000))  # Current time in milliseconds
    nonce = ''  # Leave as an empty string
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

# Fetch the list of devices
def get_device_list():
    url = 'https://api.switch-bot.com/v1.1/devices'
    headers = generate_headers()
    response = requests.get(url, headers=headers)
    return response.json()

# Fetch the status of a specific device
def get_device_status(device_id):
    url = f'https://api.switch-bot.com/v1.1/devices/{device_id}/status'
    headers = generate_headers()
    response = requests.get(url, headers=headers)
    return response.json()

# Monitor and log the device data periodically
def monitor_device(device_id, interval=60):
    print(f"Starting monitoring for device ID: {device_id}")
    while True:
        status = get_device_status(device_id)
        if status['statusCode'] == 100:
            body = status['body']
            temperature = body.get('temperature')
            humidity = body.get('humidity')
            battery = body.get('battery')
            print(f"Temperature: {temperature}°C, Humidity: {humidity}%, Battery: {battery}%")
        else:
            print("Failed to fetch status:", status)

        time.sleep(interval)  # Wait for the specified interval

# Main execution
if __name__ == '__main__':
    # Fetch the device list to identify the device IDs
    devices = get_device_list()
    print('Device List:', devices)

    # Replace 'D83038356E4E' with the device ID you want to monitor (e.g., Outdoor Meter)
    device_id = 'D5303835164E'  # Example device ID for the Outdoor Meter

    # Start monitoring the specified device
    monitor_device(device_id, interval=60)  # Fetch and log data every 60 seconds

import requests
import time
import hmac
import hashlib
import base64

# Regenerate your API token and secret key in the SwitchBot app and replace these placeholders.
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

# Main execution
if __name__ == '__main__':
    # Get the list of devices
    devices = get_device_list()
    print('Device List:', devices)

    # Example: Fetch status for a specific device
    # Replace 'your_device_id' with the actual device ID from the device list
    device_id = 'D5303835164E'  # Replace with your Outdoor Meter ID
    status = get_device_status(device_id)
    print('Device Status:', status)

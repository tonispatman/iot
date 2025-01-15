import requests
import time
import hashlib
import hmac
import base64

# Replace these with your actual token and secret
TOKEN = 'f09df5b1cf220104c6e601bcb932c69ab1cf72f51dd9153c4ddc1dbb33fc567103b5c9a020ffd1488088395495130ca5'
SECRET = '0b762c5586ff64ce2d997c96c6eb11ac'

# Generate the necessary headers for authentication
def generate_headers():
    t = int(round(time.time() * 1000))
    nonce = ''
    string_to_sign = '{}{}{}'.format(TOKEN, t, nonce)
    string_to_sign = bytes(string_to_sign, 'utf-8')
    secret = bytes(SECRET, 'utf-8')
    sign = base64.b64encode(hmac.new(secret, string_to_sign, digestmod=hashlib.sha256).digest())
    headers = {
        'Authorization': TOKEN,
        't': str(t),
        'sign': sign.decode('utf-8'),
        'nonce': nonce,
        'Content-Type': 'application/json; charset=utf8'
    }
    return headers

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

if __name__ == '__main__':
    devices = get_device_list()
    print('Devices:', devices)

    # Replace 'your_device_id' with the actual device ID of your Thermo-Hygrometer
    device_id = 'your_device_id'
    status = get_device_status(device_id)
    print('Device Status:', status)

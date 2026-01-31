import requests
import hashlib
import hmac
import time

# Replace 'YOUR_API_KEY' and 'YOUR_API_SECRET' with your actual MEXC API key and secret
API_KEY = 'mx0vglz5xFoCMXweZi'
API_SECRET = '8673af558d2d4b508c7c92bd7d0ae52a'

# Construct the request URL
url = 'https://www.mexc.com/open/api/v2/market/symbols'

# Generate a nonce (timestamp)
nonce = str(int(time.time() * 1000))

# Create the message to sign
message = f'/api/v3/exchangeInfo'

# Create the signature
signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

# Construct the request headers
headers = {
    'Content-Type': 'application/json',
    'api-key': API_KEY,
    'time': nonce,
    'sign': signature
}

# Send the GET request to the MEXC API
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Print the response data
    print(response.json())
else:
    print(f"Request failed with status code: {response.status_code}")

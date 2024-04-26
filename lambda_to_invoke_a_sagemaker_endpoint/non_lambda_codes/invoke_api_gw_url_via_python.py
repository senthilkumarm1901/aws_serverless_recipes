import requests

# Define the API Gateway URL
API_GW_URL = "your_api_gateway_url_here"

# Load JSON data from file
with open("test_event.json", "r") as f:
    payload_data = f.read()

# Set the headers
headers = {
    "Content-Type": "application/json"
}

# Send POST request
response = requests.post(API_GW_URL, headers=headers, data=payload_data)

# Print response
print(response.text)

#!/usr/bin/python
import requests
import json
import sys

# Define constants as static values that won't change
NETBOX = "localhost"
NETBOX_PORT = 8000


# Helper function to create a NetBox API URL
def create_url(path):
    return "http://%s:%s/api/%s" % (NETBOX, NETBOX_PORT, path)

# Send a GET request to the NetBox API and return response in JSON format
def get_url(path):

    # Create URL
    url = create_url(path)
    print(url)

    # Set headers for the GET request
    headers = {  
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Token 0123456789abcdef0123456789abcdef01234567'
    }

    # Send request, ignore verification of a possible SSL certificate    
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    return response.json()

# Retrieve devices' info
def get_devices():
    # Filter devices that are active and belong to NOC tenant
    return get_url("dcim/devices/?status=active&tenant=noc")


# Main function
if __name__ == "__main__":
    
    response = get_devices()

    # Create a list with devices' name from the response
    devices_name = []

    for device in response.get("results"):
        devices_name.append(device.get("name"))

    # Print out list of devices' name
    print(devices_name)
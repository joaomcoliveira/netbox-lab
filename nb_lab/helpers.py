#!/usr/bin/env python

# -------------------------------------------------------------------
# Functions to help with Nornir tasks
# -------------------------------------------------------------------

import os
import sys
import socket
from urllib.parse import urlparse
from dotenv import load_dotenv
import requests
import pynetbox
import urllib3

# Load environmental variables from .env file
load_dotenv()

# Define constants as static values that won't change
NB_URL = os.getenv("NB_URL")
NB_TOKEN = os.getenv("NB_TOKEN")
NB_CUSTOM_FIELD = os.getenv("NB_CUSTOM_FIELD")

# Disable warnings for self-signed certs if using HTTPS with NetBox
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = requests.Session()
session.verify = False

# Update a custom field in NetBox
def update_custom_field(dev_name, os_version):

    # Connect to NetBox environment
    netbox = pynetbox.api(NB_URL, token=NB_TOKEN)
    # Used with HTTPS
    netbox.http_session = session

    # Get device record from NetBox
    device = netbox.dcim.devices.get(name=dev_name)

    if NB_CUSTOM_FIELD in device.custom_fields.keys():
        # Custom field exists        
        if device.update({ "custom_fields": { NB_CUSTOM_FIELD: os_version }}):
            print(f"{dev_name}: \"{NB_CUSTOM_FIELD}\" updated with \"{os_version}\"")
        else:
            print(f"{dev_name}: \"{NB_CUSTOM_FIELD}\" not updated")
    else:
        # Custom field does not exist, need to first create it
        try:
            netbox.extras.custom_fields.create([{
                "content_types": ["dcim.device"],
                "type": "text",
                "name": NB_CUSTOM_FIELD,
                "label": "",
                "description": "",
                "required": False,
                "filter_logic": "loose",
                "default": os_version,
                "weight": 100,
                "validation_minimum": None,
                "validation_maximum": None,
                "validation_regex": "",
                "choices": []
            }])
            print(f"{dev_name}: \"{NB_CUSTOM_FIELD}\" updated with \"{os_version}\"")
        except Exception as err:
            print("Error processing request", err)
            sys.exit(1)     

def validate_nb_url(url):

    # Ensure NetBox URL starts with http:// or https://
    if not url.startswith(("http://","https://")):
        print("Scheme must be http:// or https://")
        return False

    # Splits a URL string into its components
    o = urlparse(url)

    # Ensure NetBox URL port is valid
    port = o.port

    try:
        if port < 0 or port > 65535:
            raise ValueError
    except ValueError:
        print("Port must be int 0-65535")
        return False

    # Ensure NetBox hostname is reachable
    host = o.netloc.split(":")[0]
    try:
        socket.gethostbyname(host)
    except socket.error as err:
        print(f"{err}")
        return False

    return True

def validate_nb_token(token):

    # Ensure NetBox API token is present 
    if token == "":
        print("Missing API token")
        return False
    return True

def validate_nb_custom_field(custom_field):

    # Ensure NetBox custom_field is present 
    if custom_field == "":
        print("Missing custom_field to update")
        return False
    return True


import os
import pynetbox
from dotenv import load_dotenv
from pprint import pprint


# Load environmental variables from .env file
load_dotenv()

# Define constants as static values that won't change
NB_URL = os.getenv("NB_URL")
NB_TOKEN = os.getenv("NB_TOKEN")


nb = pynetbox.api(NB_URL, token=NB_TOKEN)

devices = nb.dcim.devices.all()

for device in devices:
    print(device.name)

#pprint(dict(x))


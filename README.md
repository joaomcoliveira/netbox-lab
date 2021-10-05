# NetBox Lab

This program was developed to test NetBox's REST API, mainly to update or create a device's custom field with data collected from the device itself. In this case, custom field is "sw_version", which should represent the OS version running on the network device.

The project is built on the following components:
- pynetbox, an API client library for NetBox
- Nornir, an automation framework that executes concurrent tasks on an inventory of hosts. A NetBox plugin is used to dynamically populate this inventory based on NetBox devices' database.
- NAPALM, a library to interact with different network OS through several methods.
- Netmiko, a SSH library to access network devices' command lines.

Software version info is pulled from the devices in two ways:
1. NAPALM, using a get_facts method on supported devices (such as Cisco IOS, IOS-XR, NX-OS, Arista vEOS and Junos)
2. Netmiko, grabbing a filtered output from a platform-specific CLI command


## Requirements

1. NetBox up and running
2. Devices created with platform and management IP address

Note: Platform attribute in NetBox must match one of Netmiko or NAPALM available device type/driver (ios, eos, cisco_asa, etc.)


## Installation

1. Clone repository: `git clone https://github.com/joaomcoliveira/netbox-lab`
2. Change directory to netbox-lab: `cd netbox-lab`
3. Create a Python virtual environment: `python3 -m venv ~/virtualenvs/netbox-lab`
4. Activate the virtual environment: `source ~/virtualenvs/netbox-lab/bin/activate`
5. Install required Python packages via pip: `pip install -r requirements.txt`
6. Type `make` and ensure all tests pass

## Variables

This program uses environment variables that should be set in a `.env` file, such as NetBox URL, API token and custom field to be updated:

    NB_URL=http://urlexample:8000
    NB_TOKEN=tokenexample0123456789
    NB_CUSTOM_FIELD=sw_version

`inventory/defaults.yaml` contains default values for host inventory. Same username and password is used to connect to all devices in inventory.

`inventory/filter_params.json` sets NetBox inventory filters in JSON format.


## Testing

This project was tested on virtual appliances Cisco IOSv, ASAv, Arista vEOS and ArubaOS CX Virtual.

A `Makefile` is used for the following targets:

- `lint`: Runs `pylint` linter and the `black` formatter
- `test`: Runs unit tests on helper functions via `pytest`
- `clean`: Deletes `.pyc` and `.log` files
- `all`: Default target that runs the sequence `clean lint test`

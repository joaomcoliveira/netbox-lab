import os
from sys import platform
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command
from dotenv import load_dotenv
from nornir.core.filter import F

# Define constants as static values that won't change
NB_URL = os.getenv("NB_URL")
NB_TOKEN = os.getenv("NB_TOKEN")

# Get SW version from a Cisco ASA CLI 
def asa_get_sw_version(task):
    
    # ASA OS is supported by Netmiko, which is a SSH Python library 
    r = task.run(task=netmiko_send_command, command_string="show version | i Software Version")

    # Print os_version from the output of netmiko_send_command
    os_version = r.result 
    print(os_version)

    return None

# Get SW version from a device supported by NAPALM 
def napalm_get_sw_version(task):
    
    # NAPALM get_facts method
    # Works with EOS, Junos, IOS-XR (NETCONF), IOS-XR (XML-Agent), NX-OS and IOS
    r = task.run(task=napalm_get, getters=["facts"])

    # Print os_version from get_facts
    os_version = r.result["facts"]["os_version"] 
    print(os_version)

    return None

# Main function
def main():

    # Initialize Nornir using NetBox inventory plugin
    # Nornir host and group objects will be created from the data in NetBox database
    # Had to adapt "Platform" attribute name in NetBox to one of Netmiko's or Napalm's available device type/driver, such as: ios, eos, cisco_asa, etc. 
    nr = InitNornir(runner = {
                            "plugin": "threaded",
                            "options": {
                                # Run Nornir tasks against 10 hosts simultaneously
                                "num_workers": 10,
                            },
                        },
                        inventory = {
                            "plugin": "NetBoxInventory2",
                                "options": {
                                    "nb_url": NB_URL,
                                    "nb_token": NB_TOKEN,
                                    # Ignore verification of SSL certificate, if using https         
                                    "ssl_verify": False,
                                    # Path to file with the default definitions
                                    "defaults_file": "inventory/defaults.yaml",
                                    # Treat custom fields as a direct attribute for the host, instead of storing the value in the custom_fields attribute 
                                    "flatten_custom_fields": True,
                                    # Filter inventory data
                                    "filter_parameters": {
                                        "status": "active",
                                        "tenant": "noc"
                                    }
                                }
                    }   
            )

    # Print inventory
    print(nr.inventory.hosts.keys())

    # Filter devices by platform
    napalm_support_devices = nr.filter( F(platform__contains="ios") | 
                                        F(platform__contains="eos") | 
                                        F(platform__contains="iosxr") |
                                        F(platform__contains="iosxr_netconf") |
                                        F(platform__contains="nxos") |
                                        F(platform__contains="nxos_ssh") |
                                        F(platform__contains="junos")
                                )

    # Print inventory
    print(napalm_support_devices.inventory.hosts.keys())

    # Filter devices by platform
    netmiko_devices = nr.filter( ~F(platform__contains="ios") & 
                                        ~F(platform__contains="eos") & 
                                        ~F(platform__contains="iosxr") &
                                        ~F(platform__contains="iosxr_netconf") &
                                        ~F(platform__contains="nxos") &
                                        ~F(platform__contains="nxos_ssh") &
                                        ~F(platform__contains="junos")
                                )

    # Print inventory
    print(netmiko_devices.inventory.hosts.keys())

    # Filter devices by platform
    asa_devices = netmiko_devices.filter(F(platform__contains="asa"))

    # Print inventory
    print(asa_devices.inventory.hosts.keys())

    # Run task against our device objects
    napalm_support_devices.run(
        name="Get software version on devices supported by NAPALM",
        task=napalm_get_sw_version)

    # Run task against our device objects
    asa_devices.run(
        name="Get software version on Cisco ASA devices",
        task=asa_get_sw_version)

    return None


if __name__ == "__main__":

    # Load environmental variables from .env file
    load_dotenv()

    # Call for main function
    main()


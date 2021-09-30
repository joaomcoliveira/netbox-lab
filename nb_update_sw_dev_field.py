import os
import pynetbox
from sys import platform
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command
from dotenv import load_dotenv
from nornir.core.filter import F
from pprint import pprint

# Load environmental variables from .env file
load_dotenv()

# Define constants as static values that won't change
NB_URL = os.getenv("NB_URL")
NB_TOKEN = os.getenv("NB_TOKEN")
NB_FILTER_PARAMS = {
    "status": "active",
    "tenant": "noc"
}
NB_CUSTOM_FIELD = "sw_version"


# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------
# Get SW version from an ArubaOS CLI 
def aruba_get_sw_version(task):
    
    # ArubaOS is supported by Netmiko, which is a SSH Python library 
    r = task.run(task=netmiko_send_command, command_string="show version | i \"Version      :\"")

    # Print os_version from the output of netmiko_send_command
    os_version = r.result 

    # Call update_custom_field function
    nb_update_custom_field(f"{task.host}", os_version)

    return None


# Get SW version from a Cisco ASA CLI 
def asa_get_sw_version(task):
    
    # ASA OS is supported by Netmiko, which is a SSH Python library 
    r = task.run(task=netmiko_send_command, command_string="show version | i Software Version")

    # Assign os_version to the output of netmiko_send_command
    os_version = r.result

    # Call update_custom_field function
    nb_update_custom_field(f"{task.host}", os_version)

    return None

# Get SW version from a device supported by NAPALM 
def napalm_get_sw_version(task):
    
    # NAPALM get_facts method
    # Works with EOS, Junos, IOS-XR (NETCONF), IOS-XR (XML-Agent), NX-OS and IOS
    r = task.run(task=napalm_get, getters=["facts"])

    # Print os_version from get_facts
    os_version = r.result["facts"]["os_version"] 
    
    # Call update_custom_field function
    nb_update_custom_field(f"{task.host}", os_version)

    return None


def nb_update_custom_field(dev_name, os_version):

    nb = pynetbox.api(NB_URL, token=NB_TOKEN)

    device = nb.dcim.devices.get(name=dev_name)

    if NB_CUSTOM_FIELD in device.custom_fields.keys():
        # Custom field exists        
        if device.update({ "custom_fields": { NB_CUSTOM_FIELD: os_version }}):
            print(f"{dev_name}: \"{NB_CUSTOM_FIELD}\" updated with \"{os_version}\"")
        else:
            print(f"{dev_name}: \"{NB_CUSTOM_FIELD}\" not updated")
    else:
        # Custom field does not exist, need to first create it
        nb.extras.custom_fields.create([{
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
                                "num_workers": 1,
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
                                    "filter_parameters": NB_FILTER_PARAMS
                                }
                    }   
            )

    # -------------------------------------------------------------------
    # Filter devices in Nornir's inventory
    # -------------------------------------------------------------------
    # Filter devices supported by NAPALM
    napalm_support_devices = nr.filter( F(platform__contains="ios") | 
                                        F(platform__contains="eos") | 
                                        F(platform__contains="iosxr") |
                                        F(platform__contains="iosxr_netconf") |
                                        F(platform__contains="nxos") |
                                        F(platform__contains="nxos_ssh") |
                                        F(platform__contains="junos")
                                )
    # Filter devices not supported by NAPALM that should use Netmiko
    netmiko_devices = nr.filter( ~F(platform__contains="ios") & 
                                        ~F(platform__contains="eos") & 
                                        ~F(platform__contains="iosxr") &
                                        ~F(platform__contains="iosxr_netconf") &
                                        ~F(platform__contains="nxos") &
                                        ~F(platform__contains="nxos_ssh") &
                                        ~F(platform__contains="junos")
                                )
    # Filter devices by specific platform
    asa_devices = netmiko_devices.filter(F(platform__contains="asa"))
    # Filter devices by specific platform
    aruba_devices = netmiko_devices.filter(F(platform__contains="aruba"))


    # Debug - print inventory
    print("NetBox inventory: ", nr.inventory.hosts.keys())
    print("NAPALM supported devices: ", napalm_support_devices.inventory.hosts.keys())
    print("Netmiko devices: ", netmiko_devices.inventory.hosts.keys())
    print("ASA devices: ", asa_devices.inventory.hosts.keys())
    print("Aruba devices: ", aruba_devices.inventory.hosts.keys())

    # Run task against our device objects
    napalm_support_devices.run(
        name="Get software version on devices supported by NAPALM",
        task=napalm_get_sw_version)

    asa_devices.run(
        name="Get software version on Cisco ASA devices",
        task=asa_get_sw_version)

    aruba_devices.run(
        name="Get software version on ArubaOS devices",
        task=aruba_get_sw_version)


    return None


if __name__ == "__main__":

    # Call for main function
    main()


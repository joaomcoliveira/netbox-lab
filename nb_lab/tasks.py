#!/usr/bin/env python

# -------------------------------------------------------------------
# Nornir tasks to be used in the main runbook
# -------------------------------------------------------------------

from nornir_netmiko.tasks import netmiko_send_command
from nornir_napalm.plugins.tasks import napalm_get
from nb_lab.helpers import update_custom_field

# Get SW version from an ArubaOS CLI 
def aruba_get_sw_version(task):
    
    # ArubaOS is supported by Netmiko, which is a SSH Python library 
    res = task.run(task=netmiko_send_command, command_string="show version | i \"Version      :\"")

    # Print os_version from the output of netmiko_send_command
    os_version = res.result 

    # Call update_custom_field function
    update_custom_field(f"{task.host}", os_version)



# Get SW version from a Cisco ASA CLI 
def asa_get_sw_version(task):
    
    # ASA OS is supported by Netmiko, which is a SSH Python library 
    res = task.run(task=netmiko_send_command, command_string="show version | i Software Version")

    # Assign os_version to the output of netmiko_send_command
    os_version = res.result

    # Call update_custom_field function
    update_custom_field(f"{task.host}", os_version)


# Get SW version from a device supported by NAPALM 
def napalm_get_sw_version(task):
    
    # NAPALM get_facts method
    # Works with EOS, Junos, IOS-XR (NETCONF), IOS-XR (XML-Agent), NX-OS and IOS
    res = task.run(task=napalm_get, getters=["facts"])

    # Print os_version from get_facts
    os_version = res.result["facts"]["os_version"] 
    
    # Call update_custom_field function
    update_custom_field(f"{task.host}", os_version)

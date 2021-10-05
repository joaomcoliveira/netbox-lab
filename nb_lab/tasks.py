#!/usr/bin/env python

"""
Nornir tasks to be used in the main runbook
"""

from nornir_netmiko.tasks import netmiko_send_command
from nornir_napalm.plugins.tasks import napalm_get
from nb_lab.helpers import update_custom_field


def aruba_get_sw_version(task):
    """
    Get SW version from an ArubaOS CLI
    """
    # ArubaOS is supported by Netmiko, which is a SSH Python library
    res = task.run(
        task=netmiko_send_command, command_string='show version | i "Version      :"'
    )

    # Assign os_version from the output of netmiko_send_command
    os_version = res.result

    # Print os_version
    print(f"{task.host}: {os_version}")

    # Call update_custom_field function
    update_custom_field(f"{task.host}", os_version)


def asa_get_sw_version(task):
    """
    Get SW version from a Cisco ASA CLI
    """
    # ASA OS is supported by Netmiko, which is a SSH Python library
    res = task.run(
        task=netmiko_send_command, command_string="show version | i Software Version"
    )

    # Assign os_version from the output of netmiko_send_command
    os_version = res.result

    # Print os_version
    print(f"{task.host}: {os_version}")

    # Call update_custom_field function
    update_custom_field(f"{task.host}", os_version)


def napalm_get_sw_version(task):
    """
    Get SW version from a device supported by NAPALM
    """
    # NAPALM get_facts method
    # Works with EOS, Junos, IOS-XR (NETCONF), IOS-XR (XML-Agent), NX-OS and IOS
    res = task.run(task=napalm_get, getters=["facts"])

    # Assign os_version from get_facts
    os_version = res.result["facts"]["os_version"]

    # Print os_version
    print(f"{task.host}: {os_version}")

    # Call update_custom_field function
    update_custom_field(f"{task.host}", os_version)

#!/usr/bin/env python

"""
Main file to run the application
"""

from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
import nb_lab.tasks as t
import nb_lab.helpers as h


def main():
    """
    Entry point, execution starts here
    """
    # Initialize Nornir using NetBox inventory plugin
    # Nornir host and group objects will be created from the data in NetBox database
    # Had to adapt "Platform" attribute name in NetBox to one of Netmiko's or Napalm's available device type/driver:
    # ios, eos, cisco_asa, etc.
    nornir = InitNornir(
        runner={
            "plugin": "threaded",
            "options": {
                "num_workers": 10  # Run Nornir tasks against 10 hosts simultaneously
            },
        },
        inventory={
            "plugin": "NetBoxInventory2",
            "options": {
                "nb_url": h.NB_URL,
                "nb_token": h.NB_TOKEN,
                "ssl_verify": False,  # Ignore verification of SSL certificate, if using https
                "defaults_file": "inventory/defaults.yaml",  # Path to file with the default definitions
                "filter_parameters": h.NB_FILTER_PARAMS,  # Filter inventory data
            },
        },
    )

    # -------------------------------------------------------------------
    # Filter devices in Nornir's inventory
    # -------------------------------------------------------------------
    # Filter devices supported by NAPALM
    napalm_support_devices = nornir.filter(
        F(platform__contains="ios")
        | F(platform__contains="eos")
        | F(platform__contains="iosxr")
        | F(platform__contains="iosxr_netconf")
        | F(platform__contains="nxos")
        | F(platform__contains="nxos_ssh")
        | F(platform__contains="junos")
    )
    # Filter devices not supported by NAPALM that should use Netmiko
    netmiko_devices = nornir.filter(
        ~F(platform__contains="ios")
        & ~F(platform__contains="eos")
        & ~F(platform__contains="iosxr")
        & ~F(platform__contains="iosxr_netconf")
        & ~F(platform__contains="nxos")
        & ~F(platform__contains="nxos_ssh")
        & ~F(platform__contains="junos")
    )
    # Filter devices by specific platform
    asa_devices = netmiko_devices.filter(F(platform__contains="asa"))
    # Filter devices by specific platform
    aruba_devices = netmiko_devices.filter(F(platform__contains="aruba"))

    # Debug - print inventory
    print("NetBox inventory: ", nornir.inventory.hosts.keys())
    print("NAPALM supported devices: ", napalm_support_devices.inventory.hosts.keys())
    print("Netmiko devices: ", netmiko_devices.inventory.hosts.keys())
    print("ASA devices: ", asa_devices.inventory.hosts.keys())
    print("Aruba devices: ", aruba_devices.inventory.hosts.keys())

    # Run task against our device objects
    results = napalm_support_devices.run(
        name="Get software version on devices supported by NAPALM",
        task=t.napalm_get_sw_version,
    )

    print_result(results)

    results = asa_devices.run(
        name="Get software version on Cisco ASA devices", task=t.asa_get_sw_version
    )

    print_result(results)

    results = aruba_devices.run(
        name="Get software version on ArubaOS devices", task=t.aruba_get_sw_version
    )

    print_result(results)


if __name__ == "__main__":

    main()

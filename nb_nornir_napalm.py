import os
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get, napalm_cli
from nornir_utils.plugins.functions import print_result
from dotenv import load_dotenv

load_dotenv()

NB_URL = os.getenv("NB_URL")
NB_TOKEN = os.getenv("NB_TOKEN")

def send_command(task, cmd):
     
    task.run(task=napalm_get, getters=[cmd])

    return None


def main():
    """
    Execution begins here.
    """

    # Initialize Nornir using NetBox inventory plugin
    # Nornir host and group objects will be created from the data in NetBox database
    # We had to update "Platform" attribute in NetBox for one of netmiko's available device_type, such as: cisco_ios, cisco_asa, etc. 

    nornir = InitNornir(runner = {
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

    result = nornir.run(task=send_command, cmd="facts")
    print_result(result)

    return None



if __name__ == "__main__":
    
    main()


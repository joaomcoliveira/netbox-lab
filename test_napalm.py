import json
from napalm.base import get_network_driver

optional_args = {'transport': 'https'}
driver = get_network_driver('eos')
dev = driver(hostname='192.168.122.111', username='admin', password='admin12345', optional_args=optional_args)
dev.open()
dev_info = dev.get_facts()

print(json.dumps(dev_info, sort_keys=True, indent=4))
print(f"Facts: {dev_info}")

dev.close()

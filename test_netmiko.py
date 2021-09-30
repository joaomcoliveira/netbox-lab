from netmiko import ConnectHandler

sw12 = {
    "device_type": "aruba_osswitch",
    "ip": "192.168.122.112",
    "username": "admin",
    "password": "admin12345",    
}

net_connect = ConnectHandler(**sw12)

output = net_connect.send_command("show version")

print(output)
import ipaddress
import json
import random

def generate_subnet():
    # Choose a random starting address within RFC1918 space for each /19 subnet
    start_address = random.choice(['192.168.0.0', '172.16.0.0', '10.0.0.0'])
    subnet = ipaddress.ip_network(start_address + '/19') 
    return [str(ip) for ip in subnet]

def generate_ip_addresses():
    num_ips = random.randint(500, 600)
    subnet = generate_subnet()
    return random.sample(subnet, num_ips)

def generate_data():
    data = {}
    for i in range(1, 53):
        tenant_name = f"tenant{i}"
        data[tenant_name] = generate_ip_addresses()
    return data

data = generate_data()

# Writing data to a file
with open('output.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Data has been written to 'output.json'.")

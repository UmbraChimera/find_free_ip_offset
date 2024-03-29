import ipaddress
import sys
import json

def get_host_address(i, subnet_mask_cidr=19):
    return ipaddress.IPv4Network(f"{i}/{subnet_mask_cidr}", strict=False)

def get_offset(x, y):
    return ipaddress.ip_address(int(ipaddress.IPv4Address(x)) - int(ipaddress.IPv4Address(str(y)[:-3])))

def process_tenants(tenants_data):
    output = {}

    for tenant, ips in tenants_data.items():
        tenant_ips = {}
        used_ips = set()

        for ip in ips:
            try:
                base_network = get_host_address(ip)
                ip_address = ipaddress.IPv4Address(ip)
                if ip_address in base_network:
                    used_ips.add(str(ip_address))  
                else:
                    break
            except ipaddress.AddressValueError:
                continue

        available_ips = [str(addr) for addr in base_network.hosts() if str(addr) not in used_ips]
        offset_ips = [str(get_offset(each, base_network)) for each in available_ips]

        output[tenant] = {"available_ips": offset_ips}

    return output

def find_tenants_with_same_ips(tenants_data):
    ip_count = {}
    for data in tenants_data.values():
        for ip in data["available_ips"]:
            if ip in ip_count:
                ip_count[ip] += 1
            else:
                ip_count[ip] = 1

    all_tenants_count = len(tenants_data)
    matching_ips = [ip for ip, count in ip_count.items() if count == all_tenants_count]

    sorted_ips = sorted(matching_ips, key=lambda ip: [int(octet) for octet in ip.split('.')])

    return sorted_ips

def save_local_files(matching_offsets, available_ips_data):
    # Uncomment for testing and comment for AWX
    with open("matching_ips.txt", 'w') as file:
        file.write(matching_offsets)
    
    with open("available_ips.txt", 'w') as file:
        json.dump(available_ips_data, file, indent=4)

    # Comment for testing and uncomment for AWX
    """
    pass
    """

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("Incorrect number of arguments provided.")
        
        with open(sys.argv[1], 'r') as file:
            tenants_data = json.load(file)
        
        result = process_tenants(tenants_data)

        matching_ips = find_tenants_with_same_ips(result)
        matching_offsets = "\n".join(matching_ips)

        save_local_files(matching_offsets, result)
        
        print(matching_offsets)
        
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

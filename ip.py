import ipaddress


def get_host_address(i):
    subnet_mask_cidr = 19
    # Calculate the host address
    network = ipaddress.IPv4Network(f"{i}/{subnet_mask_cidr}", strict=False)
    x = ipaddress.IPv4Network(network)
    return (x)


def get_offset (x,y):
    i = int(x)
    y = str(y)
    y = y[:-3]
    y = int(ipaddress.IPv4Address(y))
    z = x - y
    z = ipaddress.ip_address(z)
    print (z)
    return(z)


def main():
    # Prompt for the name
    tenant = input("Enter Tenant ID (e.g., 1234):  ")
    tenant_ips = {}


    # Initialize a set to store used IP addresses
    used_ips = set()

    # Prompt the user to enter IP addresses until 'End' is entered
    print("Enter IP addresses. Enter 'End' to finish.")
    while True:
        ip = input("IP Address: ")
        if ip.lower() == 'end':
            break
        try:
            base_network = get_host_address(ip)
            ip_address = ipaddress.IPv4Address(ip)
            if ip_address in base_network:
                used_ips.add(str(ip_address))
            else:
                base_network = get_host_address(ip)
                ip_address = ipaddress.IPv4Address(ip)
                if ip_address in base_network:
                    used_ips.add(ip_address)
                else:
                    break
        except ipaddress.AddressValueError:
            print("Invalid IP address format.")
        if tenant not in tenant_ips:
            tenant_ips[tenant] = set()
        tenant_ips[tenant].add(ip_address)
        get_offset(ip_address,base_network)
        

    # Find available IP addresses
    available_ips = set(base_network.hosts()) - used_ips

    # Save available IP addresses to a file
    filename = "et" + tenant + ".txt"
    with open(filename, 'w') as file:
        file.write("Available IP addresses for ET" + str(tenant) + "\n")
        file.write(str(available_ips))

    print(f"Available IP addresses saved to '{filename}'.")

if __name__ == "__main__":
    main()
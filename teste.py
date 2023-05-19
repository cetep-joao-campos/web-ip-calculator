def addresss_to_binary(address=10):
    binary_address = []
    while address > 0:
        binary_address.insert(0, address % 2)
        address = address // 2
        while (address == 0 and len(binary_address) < 8):
            binary_address.insert(0, 0)
        print(address)
        print(binary_address)
    print(binary_address)

def cidr_to_mask(cidr):
    address_length = 0
    octet, netmask = [], []

    while address_length <= 32:
        if cidr == 0: octet.append(0)
        else: octet.append(1); cidr -= 1

        if len(octet) == 8:
            netmask.append(octet)
            octet = []

        address_length += 1

    print(netmask)
    print(len(netmask))

def identifies_network_broadcast(ip_address, netmask, cidr):
    network = []
    broadcast = []
    for i in range(len(ip_address)):
        network.append([])
        for j in range(len(ip_address[i])):
            network[i].append(ip_address[i][j] and netmask[i][j])
    
    for i in range(len(ip_address)):
        broadcast.append([])
        for j in range(len(ip_address[i])):
            print(cidr)
            if cidr == 0:
                broadcast[i].append(1)
            else:
                broadcast[i].append(network[i][j])
                cidr -= 1

    return network, broadcast



#ip_address = addresss_to_binary('')
#cidr_to_mask(24)
ip_add = [[1, 1, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1, 0], [0, 0, 0, 0, 1, 1, 0, 0]]
netmask = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]]
#identifies_network_broadcast()
#addresss_to_binary()
#print(ip_add[1])
#print(netmask[1])
#print('-' * 24)
print(identifies_network_broadcast(ip_add, netmask, 16))
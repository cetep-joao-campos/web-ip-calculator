from typing import Literal


def remount_abbreviated_ipv6_address(address: list[str]) -> list[str]:
    c = 0
    for quartet in address:
        if quartet == '':
            address.insert(c,'0000')
        if len(quartet) < 4:
            address.pop(c)
            list_quartet = list(quartet)
            while len(list_quartet) < 4:
                list_quartet.insert(0, '0')
            quartet = ''.join(list_quartet)
            address.insert(c, quartet)
        if len(address) > 8:
            del address[c+1]
        c += 1
    return address

def validate_ipv6_quartet(address: list) -> Literal[0, 1]:
    for quartet in address:
        try:
            int(quartet, 16)
        except:
            return 1
    return 0

def validate_ipv6(ipv6_without_colons: list) -> Literal[0, 1]:
    address = ipv6_without_colons
    if len(address) > 8:
        return 1
    if len(address) < 8:
        address = remount_abbreviated_ipv6_address(address)
    if validate_ipv6_quartet(address) == 1:
        return 1
    return 0

def join_binary_ipv6(ipv6: list[str]) -> list[str]:
    binary_ipv6 = list(''.join(ipv6))
    return binary_ipv6

def ipv6_to_binary(ipv6: list[str]) -> list[str]:
    binary_ipv6: list = []
    for quartet in ipv6:
        binary_quartet = format(int(quartet, base=16), '04b')
        binary_ipv6.append(binary_quartet)
    return binary_ipv6

def find_biggest_quartet_of_zeros(quartets):
    big = {'index': 0, 'lenght': 0, 'count': 0}
    index = 0
    for quartet in quartets:
        if big['lenght'] < len(quartet):
            big['index'] = index
            big['lenght'] = len(quartet)
        index += 1
        big['count'] += 1
    return big

def abbreviate_address(address: list) -> list:
    more_quartets = False # True if has more quartets after quartets of zero
    index = 0
    quartets_of_zeros = [[],]
    abbreviated_address = []
    for quartet in address:
        quartet = list(quartet)
        new_quartet = []
        nonzero = False

        for algarism in quartet:
            if (nonzero == False) and (algarism == '0'):
                continue
            else:
                nonzero = True
                new_quartet.append(algarism)
        new_quartet = ''.join(new_quartet)
        abbreviated_address.append(new_quartet)

        if new_quartet == '':
            quartets_of_zeros[-1].append(index)
        else:
            if quartets_of_zeros[-1] != []:
                quartets_of_zeros.append([])
        index += 1

    big = find_biggest_quartet_of_zeros(quartets_of_zeros)

    if len(quartets_of_zeros) - 1 > big['index']:
        more_quartets = True

    biggest_quartet_of_zeros = quartets_of_zeros.pop(big['index'])

    for quartet_indexes in quartets_of_zeros:
        for index in quartet_indexes:
            abbreviated_address[index] = '0'
    
    limiter = 1
    if not more_quartets:
        limiter = 2

    while len(biggest_quartet_of_zeros) > limiter:
        quartet_to_remove = biggest_quartet_of_zeros.pop()
        abbreviated_address.pop(quartet_to_remove)
    
    if len(abbreviated_address) < 3:
        abbreviated_address.insert(0, '')

    abbreviated_address = ':'.join(abbreviated_address)

    return abbreviated_address

def create_ipv6_quartets_list(ipv6_without_colons: list[str]) -> list[str]:
    ipv6_without_colons = list(''.join(ipv6_without_colons))
    return ipv6_without_colons

def removes_colons_from_ipv6(ipv6_add: str) -> list[str]:
    ipv6_without_colons = ipv6_add.split(':')
    return ipv6_without_colons

def separates_ipv6_from_cidr(address: str) -> list[str]:
    try:
        address_and_cidr = address.split('/')
    except:
        address_and_cidr = address
    return address_and_cidr

def address_to_str(address: list[str]) -> str:
    str_address = ''.join(address)
    return str_address

def get_ipv6_network_duoctets(binary_address: list, cidr: int) -> list:
    network = []
    for i in range(cidr):
        network.append(binary_address[i])
    return network

def bin_ipv6_addess_to_hex(ipv6_address: list):
    address = []
    duoctet = []
    quartet = []
    for bit in ipv6_address:
        quartet.append(bit)
        if len(quartet) == 4:
            dec_quartet = int(''.join(quartet), base=2)
            duoctet.append(hex(dec_quartet)[2:])
            quartet = []
        if len(duoctet) == 4:
            address.append(''.join(duoctet))
            duoctet = []
    return address

def get_network_and_host_min(network):
    host_min = network.copy()
    while len(host_min) < 128:
        host_min.append('0')
    hex_host_min = bin_ipv6_addess_to_hex(host_min)
    return hex_host_min

def get_host_max(network):
    host_max = network.copy()
    while len(host_max) < 128:
        host_max.append('1')
    hex_host_max = bin_ipv6_addess_to_hex(host_max)
    return hex_host_max

def get_ipv6_netinfo(address: str) -> dict:
    abbreviated_ipv6_address: str
    full_address: str
    full_network: str
    network: str
    host_min: str
    host_max: str
    hosts_per_net: str
    ip_and_cidr: list = separates_ipv6_from_cidr(address)
    ipv6_add: str
    cidr: int
    net_info: dict

    if len(ip_and_cidr)== 1:
        ipv6_add = ip_and_cidr[0]
        cidr = None
    else:
        ipv6_add = ip_and_cidr[0]
        cidr = int(ip_and_cidr[1])

    ipv6_without_colons = removes_colons_from_ipv6(ipv6_add)
    if len(ipv6_without_colons) < 8:
        ipv6_without_colons = remount_abbreviated_ipv6_address(
            ipv6_without_colons)

    full_address = address_to_str(':'.join(ipv6_without_colons))

    if validate_ipv6(ipv6_without_colons) == 1:
        return 1
    
    abbreviated_ipv6_address = abbreviate_address(ipv6_without_colons)
    list_ipv6_quartets = create_ipv6_quartets_list(ipv6_without_colons)

    try:
        binary_ipv6_add = join_binary_ipv6(ipv6_to_binary(list_ipv6_quartets))
    except:
        return 1

    if cidr == None:
        net_info = {
            'Full address': full_address,
            'Address': abbreviated_ipv6_address,
        }
    else:
        network_bits = get_ipv6_network_duoctets(binary_ipv6_add, cidr)
        full_network = get_network_and_host_min(network_bits)
        host_min = get_network_and_host_min(network_bits)
        host_max = get_host_max(network_bits)
        network = abbreviate_address(full_network)
        hosts_per_net = 2**(128 - cidr)
 
        net_info = {
            'Endereço completo': full_address,
            'Endereço': abbreviated_ipv6_address,
            'Rede completa': ':'.join(full_network),
            'Rede':  f'{network}/{cidr}',
            'Host min': ':'.join(host_min),
            'Host max': ':'.join(host_max),
            'Hosts/rede': f'2^({128 - cidr}) = {hosts_per_net}',
        }
    return net_info

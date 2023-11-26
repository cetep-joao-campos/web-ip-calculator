# IPv4 functions

def get_formated_binary_address(binary_address: list):
    formated_binary_address = []
    for octet in binary_address:
        formated_octet = ''.join(str(bit) for bit in octet)
        formated_binary_address.append(formated_octet)
    formated_binary_address = '.'.join(formated_binary_address)
    return formated_binary_address

def get_hosts_per_subnet(cidr):
    if cidr == 32:
        hosts_per_subnet = 1
    elif cidr == 31:
        hosts_per_subnet = 0
    elif cidr == 30:
        hosts_per_subnet = 2
    else:
        hosts_bits = 32 - cidr
        hosts_per_subnet = (2 ** hosts_bits) - 2
    return hosts_per_subnet


def address_to_binary(address: list) -> list:
    binary_address = []
    for octet in address:
        binary_octet = []
        while (octet > 0 or len(binary_octet) < 8):
            binary_octet.insert(0, octet % 2)
            octet = octet // 2
            if octet == 0 and len(binary_octet) < 8:
                binary_octet.insert(0, 0)

        binary_address.append(binary_octet)
    return binary_address

def cidr_to_mask(cidr: int) -> list:
    address_length = 0
    octet, binary_netmask = [], []

    while address_length <= 32:
        if cidr == 0: octet.append(0)
        else: octet.append(1); cidr -= 1

        if len(octet) == 8:
            binary_netmask.append(octet)
            octet = []

        address_length += 1
    return binary_netmask

def address_to_integer(address, type_of_mask=''):
    if type_of_mask == 'CIDR':
        address = int(address)
    else:
        for octet in address:
            if len(address) > 0:
                octet = int(address.pop(0))
                address_to_integer(address)
                address.insert(0, octet)
    return address

def validate_ip(address: str, type_of_mask=''):
    if type_of_mask == 'CIDR':
        address = address_to_integer(address, type_of_mask)
    else:
        list_address = address.split(".")
        address = []

        while len(list_address) > 0:
            address.append(list_address.pop(0))
    
        address = address_to_integer(address)

        # verificar possibilidade de criar códigos de erros
        # por enquanto, retornará `None`
        if len(address) == 2:
            if (address < 0) or (address > 32):
                return 1
        elif len(address) != 4:
            return 1
        else:
            for octet in address:
                if (octet < 0) or (octet > 255):
                    return "InvalidIP"
    return address

def get_network(binary_ip, binary_netmask):
    binary_network = []
    for i in range(len(binary_ip)):
        binary_network.append([])
        for j in range(len(binary_ip[i])):
            binary_network[i].append(binary_ip[i][j] and binary_netmask[i][j])
    return binary_network

def get_broadcast(binary_ip, binary_network, cidr):
    binary_broadcast = []
    for i in range(len(binary_ip)):
        binary_broadcast.append([])
        for j in range(len(binary_ip[i])):
            if cidr == 0:
                binary_broadcast[i].append(1)
            else:
                binary_broadcast[i].append(binary_network[i][j])
                cidr -= 1
    return binary_broadcast

def get_cidr(netmask):
    cidr = 0
    binary_netmask = address_to_binary(netmask)
    for octet in binary_netmask:
        for bit in octet:
            if bit == 1:
                cidr += 1
    return cidr

def binary_to_decimal(address: list):
    decimal_ip = []
    delimiter = '.'
    for octet in address:
        decimal_octet = 0
        exponent = 7
        for bit in octet:
           decimal_octet += bit * (2 ** exponent) 
           exponent -= 1
        decimal_ip.append(str(decimal_octet))
    return delimiter.join(decimal_ip)

def get_first_host(binary_network):
    binary_first_host = [octet[:] for octet in binary_network]
    binary_first_host[-1][-1] = 1
    return binary_first_host

def get_last_host(binary_broadcast):
    binary_last_host = [octet[:] for octet in binary_broadcast]
    binary_last_host[-1][-1] = 0
    return binary_last_host

def identify_special_address(address: list, cidr: int) -> str:
    special_address = None
    if ((address[0] == 0)
            and (address[1] == 0)
            and (address[2] == 0)
            and (address[3] == 0)):
        special_address = 'This host on this network'
    elif address[0] == 10:
        special_address = 'Private use'
    elif address[0] == 127:
        special_address = 'Loopback address'
    elif (address[0] == 169
            and address[1] == 254):
        special_address = 'Link Local - APIPA (Automatic Private IP Addressing)'
    elif ((address[0] == 172)
            and (address[1] >= 16)
            and (address[1] <= 31)):
        special_address = 'Private use'
    elif (address[0] == 192
          and address[1] == 0
          and address[1] == 0):
        special_address = 'IETF Protocol Assignments'
    elif (address[0] == 192 
            and address[1] == 0
            and address[2] == 2):
        special_address = 'Documentation (TEST-NET-1) RFC 3330 https://datatracker.ietf.org/doc/html/rfc3330'
    elif (address[0] == 192
          and address[1] == 88
          and address[2] == 99):
        special_address = '6to4 Relay anycast'
    elif (address[0] == 192
            and address[1] == 168):
        special_address = 'Private use'
    elif (address[0] == 198
          and (address[1] == 18
               or address[1] == 19)):
        special_address = 'Benchmarking'
    elif (address[0] == 198
            and address[1] == 51
            and address[2] == 100):
        special_address = 'Documentation (TEST-NET-2) RFC 5737 https://www.rfc-editor.org/rfc/rfc5737'
    elif (address[0] == 203
          and address[1] == 0
          and address[2] == 113):
        special_address = 'Documentation (TEST-NET-3) RFC 5737 https://www.rfc-editor.org/rfc/rfc5737'
    elif (address[0] == 224
            and address[1] == 0
            and address[2] == 0
            and address[3] == 1):
        special_address = 'Multicast (all nodes)'
    elif (address[0] == 224
            and address[1] == 0
            and address[2] == 0
            and address[3] == 2):
        special_address = 'Multicast (all routers)'
    elif (address[0] >= 224
          and address[0] <= 239):
        special_address = 'Multicast'
    elif (address[0] >= 240
          and address[0] <= 255):
        special_address = 'Reserved for Future Use'
    elif (address[0]
            and address[1]
            and address[2]
            and address[3] == 255
            and cidr == 32):
        special_address = 'Limited broadcast (non-routable)'
    else:
        special_address = 'Internet'

    return special_address

def get_netinfo(address_with_mask: str) -> dict:
    net_info = {}
    TYPES_OF_NETMASKS: tuple[str] = ('NETMASK', 'CIDR')

    if len(address_with_mask) > 18:
        address_with_mask = address_with_mask.split()
        type_of_mask = TYPES_OF_NETMASKS[0]
    else:
        address_with_mask = address_with_mask.split('/')
        type_of_mask = TYPES_OF_NETMASKS[1]
        cidr = validate_ip(address_with_mask[1], type_of_mask)
        binary_netmask = cidr_to_mask(cidr)

    ip_address = validate_ip(address_with_mask[0])
    if type_of_mask == 'NETMASK':
        netmask = validate_ip(address_with_mask[1], type_of_mask)
        binary_netmask = address_to_binary(netmask)
        cidr = get_cidr(netmask)

    binary_ip = address_to_binary(ip_address)
    binary_network = get_network(binary_ip, binary_netmask)
    binary_broadcast = get_broadcast(binary_ip, binary_network, cidr)
    binary_first_host = get_first_host(binary_network)
    binary_last_host = get_last_host(binary_broadcast)
    decimal_ip = binary_to_decimal(binary_ip)
    decimal_netmask = binary_to_decimal(binary_netmask)
    decimal_network = '/'.join([binary_to_decimal(binary_network), str(cidr)])
    decimal_broadcast = binary_to_decimal(binary_broadcast)
    decimal_first_host = binary_to_decimal(binary_first_host)
    decimal_last_host = binary_to_decimal(binary_last_host)
    hosts_p_subnet = get_hosts_per_subnet(cidr)
    decimal_ip_list = address_to_integer(decimal_ip.split('.'))

    if decimal_ip == '255.255.255.255' and cidr == 32:
        net_info: dict = {
            'Address': decimal_ip,
            'Special address': 'Limited broadcast (non-routable)'
        }
    else:
        net_info: dict = {
            'Endereço': decimal_ip,
            'Rede': decimal_network,
            'Máscara': decimal_netmask,
            'Broadcast': decimal_broadcast,
            'Primeiro Host': decimal_first_host,
            'Último Host': decimal_last_host,
            'Hosts/rede': hosts_p_subnet,
            'Endereço especial': identify_special_address(decimal_ip_list, cidr),
            'Endereço Bin': get_formated_binary_address(binary_ip),
            'Rede Bin': get_formated_binary_address(binary_network),
            'Máscara Bin': get_formated_binary_address(binary_netmask),
            'Broadcast Bin': get_formated_binary_address(binary_broadcast),
            'Primeiro Host Bin': get_formated_binary_address(binary_first_host),
            'Último Host Bin': get_formated_binary_address(binary_last_host),
        }

    return net_info

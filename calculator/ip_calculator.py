def get_formated_binary_address(binary_address: list):
    formated_binary_address = []
    for octet in binary_address:
        formated_octet = ''.join(str(bit) for bit in octet)
        formated_binary_address.append(formated_octet)
    formated_binary_address = '.'.join(formated_binary_address)
    return formated_binary_address

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
                print("CIDR inválido.")
                return None
        elif len(address) != 4:
            print("Endereço IP incorreto. Número de octets (4 obrigatoriamente) inválido")
            return None
        else:
            for octet in address:
                if (octet < 0) or (octet > 255):
                    print("Endereço IP ou máscara de rede incorreto. octeto fora do intervalo de 0 - 255.")
                    return None
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

def get_netinfo(address_with_mask: str):
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

    net_info: dict = {
        'Address': decimal_ip,
        'Network': decimal_network,
        'Netmask': decimal_netmask,
        'Broadcast': decimal_broadcast,
        'First Host': decimal_first_host,
        'Last Host': decimal_last_host,
        '0bAddress': get_formated_binary_address(binary_ip),
        '0bNetwork': get_formated_binary_address(binary_network),
        '0bNetmask': get_formated_binary_address(binary_netmask),
        '0bBroadcast': get_formated_binary_address(binary_broadcast),
        '0bFirst Host': get_formated_binary_address(binary_first_host),
        '0bLast Host': get_formated_binary_address(binary_last_host),
    }

    return net_info
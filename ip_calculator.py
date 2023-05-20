def address_to_binary(address: list) -> list:
    binary_address = []
    for octet in address:
        binary_octet = []
        while (octet > 0 or len(binary_octet) < 8):
            binary_octet.insert(0, octet % 2)
            octet = octet // 2
            #while (octet == 0 and len(binary_octet) < 8):
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

def main(address_with_mask: str):
    TYPES_OF_NETMASKS: tuple[str] = ('NETMASK', 'CIDR')

    if len(address_with_mask) > 18:
        address_with_mask = address_with_mask.split()
        type_of_mask = TYPES_OF_NETMASKS[0]
    else:
        address_with_mask = address_with_mask.split('/')
        type_of_mask = TYPES_OF_NETMASKS[1]
        cidr = validate_ip(address_with_mask[1], type_of_mask)
        binary_mask = cidr_to_mask(cidr)

    ip_address = validate_ip(address_with_mask[0])
    if type_of_mask == 'NETMASK':
        netmask = validate_ip(address_with_mask[1], type_of_mask)
        binary_mask = address_to_binary(netmask)

    binary_ip = address_to_binary(ip_address)

    binary_network = get_network(binary_ip, binary_mask)
    binary_broadcast = get_broadcast(binary_ip, binary_network, cidr)

    print(binary_ip)
    print(binary_mask)
    print(binary_network)
    print(binary_broadcast)



#main('192.168.0.1 255.255.255.0')
main('192.168.0.1/24')
#separate_ip_from_mask('192.168.0.1/24')
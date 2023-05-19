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

def validate_ip(address: str, type_of_mask='') -> list:
    if type_of_mask == 'CIDR':
        address = address_to_integer(address, type_of_mask)
    else:
        list_address = address.split(".")
        address = []

        while len(list_address) > 0:
            address.append(list_address.pop(0))
    
        address = address_to_integer(address)

        if len(address) == 2:
            if (address < 0) or (address > 32):
                print("CIDR inválido.")
        elif len(address) != 4:
            print("Endereço IP incorreto. Número de octets (4 obrigatoriamente) inválido")
        else:
            for octet in address:
                if (octet < 0) or (octet > 255):
                    print("Endereço IP ou máscara de rede incorreto. octeto fora do intervalo de 0 - 255.")
        
    return address


# - [ ] converter endereço para binário
# - [ ] converter CIDR para máscara de subrede

def addresss_to_binary(address=255):
    binary_address = 0
    while address > 0:
        address = address // 2
        print(address)

def separate_ip_from_mask(address_with_mask: str):
    TYPES_OF_NETMASKS: tuple[str] = ('MASK', 'CIDR')

    if len(address_with_mask) > 18:
        address_with_mask = address_with_mask.split()
        type_of_mask = TYPES_OF_NETMASKS[0]
    else:
        address_with_mask = address_with_mask.split('/')
        type_of_mask = TYPES_OF_NETMASKS[1]

    #ip_address = validate_ip(address_with_mask[0])
    ip = address_with_mask[0]
    mask = address_with_mask[1]
    netmask = validate_ip(mask, type_of_mask)


    print(netmask)


separate_ip_from_mask('192.168.0.1 255.255.255.0')
#separate_ip_from_mask('192.168.0.1/24')
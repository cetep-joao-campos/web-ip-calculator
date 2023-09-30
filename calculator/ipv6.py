def reduce_quartet(
        abbreviated_address: list,
        quartets_reduce: dict,
        biggest_quartet: dict) -> list:
    for k in quartets_reduce.keys():
        if k != biggest_quartet.keys():
            abbreviated_address[k] == '0'
        else:
            abbreviated_address[k] == ''
    return abbreviated_address

def find_quartets_to_reduce(quartets):
    big = {}
    quartets_to_reduce = {}
    index = 0
    for quartet in quartets:
        big[index] = len(quartet)
    
    for k, v in big.items():
        if v > 1:
            quartets_to_reduce[k] = v
    return quartets_to_reduce

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
    print('Address:')
    print(address)
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

def remount_abbreviated_ip6_address(address: list) -> list:
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

def validate_ip6_quartet(address: list) -> int:
    for quartet in address:
        try:
            int(quartet, 16)
        except:
            return 1
    return 0

def validate_ip6(address: str) -> list:
    list_address = address.split(':')
    if len(list_address) > 8:
        return 1
    if len(list_address) < 8:
        list_address = remount_abbreviated_ip6_address(list_address)
    if validate_ip6_quartet(list_address) == 1:
        print("Invalid IPv6 address.")
    return list_address

def get_ipv6_netinfo(address: str):
    if validate_ip6(address) == 1:
        print("This is not a valid IPv6.")
    else:
        print(abbreviate_address(validate_ip6(address)))

ip6 = "2001:0db8:cafe:0000:8e70:5aff:feee:10ac"
ip6_1 = "2001:0db8:cafe::feee:10ac"
ip6_2 = "2001:db8::b1"
ip6_3 = "2001:0db8:cafe:0000:8e70:5aff:feee:10ag"
ip6_4 = "0db8:cafe:0000:0000:ab0f:00a1"
ip6_5 = "0db8:cafe:0000:0000:ab0f:0000:0000:0000"
ip6_6 = "0000:0ab0:0000:ab0f:0000:0000:a1ef:0000"
ip6_7 = "2001:0db8:0000:0000:0000:0000:0000:00b1"
ip6_8 = "db8:cafe:0:0:ab0f::"
ip6_9 = "0:ab0:0:ab0f::a1ef:0"
ip6_10 = "0000:ab0:0000:ab0f::a1ef:0000"
ip6_11 = 'ff02::1'
ip6_12 = '::1'

get_ipv6_netinfo(ip6_12)
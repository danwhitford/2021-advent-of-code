import aoc2021.day16 as day16


def test_adder1():
    assert day16.adder(2, 5) == 7


def test_expand1():
    assert day16.expand('D2FE28') == '110100101111111000101000'


def test_readliteral1():
    s = '110100101111111000101000'
    reader = day16.Reader(s)
    packet = reader.read_packet()
    assert packet['version'] == 6
    assert packet['type'] == 'literal'
    assert packet['val'] == 2021


def test_readoperator1():
    s = '00111000000000000110111101000101001010010001001000000000'
    reader = day16.Reader(s)
    packet = reader.read_packet()
    assert packet['version'] == 1
    assert packet['type_id'] == 6
    assert packet['type'] != 'literal'

    children = packet['children']
    assert len(children) == 2
    assert children[0]['val'] == 10
    assert children[1]['val'] == 20


def test_readoperator2():
    s = '11101110000000001101010000001100100000100011000001100000'
    reader = day16.Reader(s)
    packet = reader.read_packet()
    assert packet['version'] == 7
    assert packet['type_id'] == 3
    assert packet['type'] != 'literal'

    children = packet['children']
    assert len(children) == 3
    assert children[0]['val'] == 1
    assert children[1]['val'] == 2
    assert children[2]['val'] == 3


def test_nested1():
    h = '8A004A801A8002F478'
    s = day16.expand(h)
    reader = day16.Reader(s)
    packet = reader.read_packet()
    assert packet['type'] != 'literal'
    assert packet['version'] == 4

    children = packet['children']
    assert children[0]['type'] != 'literal'
    assert children[0]['version'] == 1

    assert children[0]['children'][0]['type'] != 'literal'
    assert children[0]['children'][0]['version'] == 5

    assert children[0]['children'][0]['children'][0]['type'] == 'literal'
    assert children[0]['children'][0]['children'][0]['version'] == 6

    assert day16.sum_versions(packet) == 16


def test_nested2():
    h = '620080001611562C8802118E34'
    s = day16.expand(h)
    reader = day16.Reader(s)
    packet = reader.read_packet()
    assert packet['type'] != 'literal'
    assert packet['version'] == 3

    children = packet['children']
    assert len(children) == 2

    assert children[0]['type'] != 'literal'
    assert children[1]['type'] != 'literal'

    assert children[0]['children'][0]['type'] == 'literal'
    assert children[0]['children'][1]['type'] == 'literal'

    assert children[1]['children'][0]['type'] == 'literal'
    assert children[1]['children'][1]['type'] == 'literal'

    assert day16.sum_versions(packet) == 12


def test_nested3():
    h = 'C0015000016115A2E0802F182340'
    s = day16.expand(h)
    reader = day16.Reader(s)
    packet = reader.read_packet()
    assert day16.sum_versions(packet) == 23


def test_nested4():
    h = 'A0016C880162017C3686B18A3D4780'
    s = day16.expand(h)
    reader = day16.Reader(s)
    packet = reader.read_packet()
    assert day16.sum_versions(packet) == 31

def test_calculator1():
    h = 'C200B40A82'
    s = day16.expand(h)
    reader = day16.Reader(s)
    packet = reader.read_packet()
    assert day16.eval_packet(packet) == 3   


def test_calculator2():
    h = '04005AC33890'
    s = day16.expand(h)
    reader = day16.Reader(s)
    packet = reader.read_packet()
    assert day16.eval_packet(packet) == 54   


def test_calculator3():
    h = '880086C3E88112'
    s = day16.expand(h)
    reader = day16.Reader(s)
    packet = reader.read_packet()
    assert day16.eval_packet(packet) == 7


def test_calculator4():
    h = 'CE00C43D881120'
    s = day16.expand(h)
    reader = day16.Reader(s)
    packet = reader.read_packet()
    assert day16.eval_packet(packet) == 9   


def test_calculator5():
    h = 'D8005AC2A8F0'
    s = day16.expand(h)
    reader = day16.Reader(s)
    packet = reader.read_packet()
    assert day16.eval_packet(packet) == 1   


def test_calculator6():
    h = 'F600BC2D8F'
    s = day16.expand(h)
    reader = day16.Reader(s)
    packet = reader.read_packet()
    assert day16.eval_packet(packet) == 0   


def test_calculator7():
    h = '9C005AC2F8F0'
    s = day16.expand(h)
    reader = day16.Reader(s)
    packet = reader.read_packet()
    assert day16.eval_packet(packet) == 0   


def test_calculator8():
    h = '9C0141080250320F1802104A08'
    s = day16.expand(h)
    reader = day16.Reader(s)
    packet = reader.read_packet()
    assert day16.eval_packet(packet) == 1  

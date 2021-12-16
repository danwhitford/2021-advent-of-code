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

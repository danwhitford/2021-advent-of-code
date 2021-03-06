import os.path
import math
from functools import reduce

hex_map = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

type_map = {
    0: 'sum',
    1: 'product',
    2: 'min',
    3: 'max',
    4: 'literal',
    5: 'gt',
    6: 'lt',
    7: 'eq',
}


def expand(hex_string):
    return ''.join(
        [hex_map.get(h, '') for h in hex_string]
    )


def sum_versions(packet):
    total = 0
    total += packet['version']

    if packet['type'] != 'literal':
        for child in packet['children']:
            total += sum_versions(child)

    return total


def eval_packet(packet):
    t = packet['type']
    if t == 'literal':
        return packet['val']
    elif t == 'sum':
        return sum([eval_packet(p) for p in packet['children']])
    elif t == 'product':
        return reduce(lambda a, b: a*b, [eval_packet(p) for p in packet['children']])
    elif t == 'min':
        return min([eval_packet(p) for p in packet['children']])
    elif t == 'max':
        return max([eval_packet(p) for p in packet['children']])
    elif t == 'gt':
        return 1 if eval_packet(packet['children'][0]) > eval_packet(packet['children'][1]) else 0
    elif t == 'lt':
        return 1 if eval_packet(packet['children'][0]) < eval_packet(packet['children'][1]) else 0
    elif t == 'eq':
        return 1 if eval_packet(packet['children'][0]) == eval_packet(packet['children'][1]) else 0


class Reader():
    def __init__(self, packet_string):
        self.curr = 0
        self.src = packet_string

    def read_packet(self):
        version = int(self.read_n(3), 2)
        packet_id = int(self.read_n(3), 2)
        packet_type = type_map.get(packet_id, 'operator')

        if packet_id == 4:
            val = self.read_val()
            return {
                'version': version,
                'type_id': packet_id,
                'type': packet_type,
                'val': val,
            }
        else:
            packets = []
            length_type_id = self.read()
            if length_type_id == '0':
                l = int(self.read_n(15), 2)
                read_up_to = self.curr + l
                while self.curr < read_up_to:
                    packets.append(self.read_packet())
            elif length_type_id == '1':
                l = int(self.read_n(11), 2)
                packets_to_read = l
                while len(packets) < packets_to_read:
                    packets.append(self.read_packet())
            return {
                'version': version,
                'type_id': packet_id,
                'type': packet_type,
                'children': packets,
            }

    def read(self):
        c = self.src[self.curr]
        self.curr += 1
        return c

    def read_n(self, n):
        s = ''
        for i in range(n):
            s += self.read()
        return s

    def read_val(self):
        s = ''
        while True:
            bits = self.read_n(5)
            s += bits[1:]
            if bits[0] != '1':
                break
        return int(s, 2)

import json
if __name__ == '__main__':
    with open(os.path.dirname(__file__) + '/res/day16') as f:
        s = f.read()
        h = expand(s)
        reader = Reader(h)
        packet = reader.read_packet()
        print(eval_packet(packet))

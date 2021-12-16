
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
    4: 'literal'
}

def adder(a, b):
    return a+b


def expand(hex_string):
    return ''.join(
        [hex_map[h] for h in hex_string]
    )

class Reader():
    def __init__(self, packet_string):
        self.curr = 0
        self.src = packet_string

    def read_packet(self):
        version = int(self.read_n(3), 2)
        type = type_map.get(int(self.read_n(3), 2), 'operator')
        return {
            'version': version,
            'type': type,
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

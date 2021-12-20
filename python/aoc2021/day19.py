import itertools
import math
import os
class Vector():
    def __init__(self,start,end,vec):
        self.start = start
        self.end = end
        self.vec = vec

class Point():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def vector_to(self, other):
        return (other.x-self.x, other.y-self.y, other.z-self.z)

    def manhatten_distance(self, other):
        return math.sqrt(((other.x - self.x) * (other.x - self.x)) + ((other.y - self.y) * (other.y - self.y)) + ((other.z - self.z) * (other.z - self.z)))

    def vector_list(self, others):
        return [self.vector_to(p) for o in others]

    def add_points(self, triple):
        return Point(self.x + triple[0], self.y + triple[1], self.z + triple[2])

    def __repr__(self):
        return f'[P {self.x} {self.y} {self.z}]'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))


class Scanner():
    def __init__(self, id, beacons):
        self.id = id
        self.beacons = beacons

    def vector_map(self):
        m = {}
        for a in self.beacons:
            al = set()
            for b in self.beacons:
                if a == b: continue
                al.add(a.manhatten_distance(b))
            m[a] = al
        return m

    def get_overlaps(self, other):
        self_vectors = self.vector_map()
        overlaps = []
        for point, point_vector in other.vector_map().items():
            for self_point, self_point_vector in self_vectors.items():
                if point == self_point: continue
                intersection = self_point_vector.intersection(point_vector)
                if len(intersection) > 1:
                    overlaps.append((self_point, point))
        return overlaps


class StarMap():
    def __init__(self, scanners):
        self.scanners = scanners
        self.position_table = {}
        self.positions = set()

    def resolve_pos(self, pos):
        ...

    def get_all_beacons(self):
        for a in self.scanners:
            for b in self.scanners:
                if a == b: continue
                overlaps = a.get_overlaps(b)
                if len(overlaps) >= 12:
                    for a_pos, b_pos in overlaps:
                        self.positions.add((a.id, a_pos))
                else:
                    self.positions.update({(a.id, p) for p in a.beacons if p not in [o[1] for o in overlaps]})

        
        print(self.positions)
        return self.positions


def parse_input(s):
    n = 0
    points = []
    scanners = []
    scanner = None
    for line in s.splitlines():
        line = line.strip()
        if len(line) < 1:
            if len(points) > 0:
                scanners.append(Scanner(n, points))
                scanner = None
                points = []
                n += 1
        elif line.startswith('---'):
            points = []
        else:
            x,y,z = [int(c) for c in line.split(',')]
            points.append(Point(x,y,z))
    if len(points) > 0:
        scanners.append(Scanner(n, points))
    return scanners


if __name__ == '__main__':
    with open(os.path.dirname(__file__) + '/res/day19') as f:
        s = f.read()
        scanners = parse_input(s)
        starmap = StarMap(scanners)
        print(len(starmap.get_all_beacons()))
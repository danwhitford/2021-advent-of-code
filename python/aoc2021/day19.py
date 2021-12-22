import itertools
import math
import os


class Vector():
    def __init__(self, start, end, vec):
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

    def euclidean_distance(self, other):
        return math.sqrt(((other.x - self.x) * (other.x - self.x)) + ((other.y - self.y) * (other.y - self.y)) + ((other.z - self.z) * (other.z - self.z)))

    def manhatten_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def vector_list(self, others):
        return [self.vector_to(p) for o in others]

    def add_point(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def minus_point(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def _get_rotations(self, x, y, z):
        o = [
            [x, y, z, ],
            [-x, y, z, ],
            [x, -y, z, ],
            [x, y, -z, ],
            [-x, -y, z, ],
            [-x, y, -z, ],
            [x, -y, -z, ],
            [-x, -y, -z, ],
        ]
        rotations = []
        for oo in o:
            rotations += [Point(x, y, z)
                          for x, y, z in itertools.permutations(oo, 3)]
        return rotations

    def get_rotations(self):
        return self._get_rotations(self.x, self.y, self.z)

    def __repr__(self):
        return f'(P {self.x} {self.y} {self.z})'

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
                if a == b:
                    continue
                al.add(a.euclidean_distance(b))
            m[a] = al
        return m

    def get_overlaps(self, other):
        self_vectors = self.vector_map()
        overlaps = []
        for point, point_vector in other.vector_map().items():
            for self_point, self_point_vector in self_vectors.items():
                if point == self_point:
                    continue
                intersection = self_point_vector.intersection(point_vector)
                if len(intersection) > 2:
                    overlaps.append((self_point, point))
        return overlaps


class StarMap():
    def __init__(self, scanners):
        self.scanners = scanners
        self.sentinal = scanners[0]
        self.scanner_locations = set()

    def _get_all_beacons(self):
        for other in self.scanners[1:]:
            overlaps = self.sentinal.get_overlaps(other)
            if len(overlaps) >= 12:
                rotated_overlaps = []
                for a_pos, b_pos in overlaps:
                    # print(f'Overlapping {a_pos} {b_pos}')
                    # One rotation ALWAYS MATCHES at same index
                    rotated_overlaps.append(
                        [a_pos.add_point(pnt) for pnt in b_pos.get_rotations()])
                correct_rotation_index = None
                station_pos = None
                for i in range(48):
                    a = [aa[i] for aa in rotated_overlaps]
                    if len(set(a)) == 1:
                        correct_rotation_index = i
                        break
                station_pos = rotated_overlaps[0][correct_rotation_index]
                print(f'Station pos {station_pos}')
                self.scanner_locations.add(station_pos)
                for b_pos in other.beacons:
                    converted = station_pos.minus_point(
                        b_pos.get_rotations()[correct_rotation_index])
                    self.sentinal.beacons.add(converted)

    def get_all_beacons(self):
        l = len(self.sentinal.beacons)
        while True:
            self._get_all_beacons()
            if l == len(self.sentinal.beacons):
                break
            else:
                l = len(self.sentinal.beacons)
        return self.sentinal.beacons

    def get_largest_manhattan_distance(self):
        l = len(self.sentinal.beacons)
        while True:
            self._get_all_beacons()
            if l == len(self.sentinal.beacons):
                break
            else:
                l = len(self.sentinal.beacons)
        max_md = 0
        for a in self.scanner_locations:
            for b in self.scanner_locations:
                if a == b:
                    continue
                md = a.manhatten_distance(b)
                if md > max_md:
                    max_md = md
        return max_md


def parse_input(s):
    n = 0
    points = set()
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
            points = set()
        else:
            x, y, z = [int(c) for c in line.split(',')]
            points.add(Point(x, y, z))
    if len(points) > 0:
        scanners.append(Scanner(n, points))
    return scanners


if __name__ == '__main__':
    with open(os.path.dirname(__file__) + '/res/day19') as f:
        s = f.read()
        scanners = parse_input(s)
        starmap = StarMap(scanners)
        print(len(starmap.get_all_beacons()))
        print(starmap.get_largest_manhattan_distance())

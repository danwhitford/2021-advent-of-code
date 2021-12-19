
class Point():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def facings(self, a, b, c):
        return [
            Point(a, b, c),
            Point(-a, -b, -c),
            Point(-a, b, c),
            Point(a, -b, c),
            Point(a, b, -c),
            Point(-a, -b, c),
            Point(-a, b, -c),
            Point(a, -b, -c),
        ]

    def vector_to(self, other):
        return (other.x-self.x, other.y-self.y, other.z-self.z)

    def vector_list(self, others):
        return [self.vector_to(p) for o in others]

    def orientations(self):
        a, b, c = abs(self.x), abs(self.y), abs(self.z)
        perspectives = [
            *self.facings(a, b, c),
            *self.facings(a, c, b),
            *self.facings(b, a, c),
            *self.facings(b, c, a),
            *self.facings(c, a, b),
            *self.facings(c, b, a),
        ]
        return perspectives


class Scanner():
    def __init__(self, id, beacons):
        self.id = id
        self.beacons = beacons

    def orientations(self):
        pz = [p.orientations() for p in self.beacons]
        os = []
        for o in list(map(list, zip(*pz))):
            os.append(Scanner(self.id, o))
        return os

    def vector_map(self):
        m = {}
        for a in self.beacons:
            al = set()
            for b in self.beacons:
                if a == b: continue
                al.add(a.vector_to(b))
            m[a] = al
        return m

    def get_overlaps(self, other):
        overlaps = set()
        self_vectors = self.vector_map()
        for orientation in other.orientations():
            for point, point_vector in orientation.vector_map().items():
                for self_point, self_point_vector in self_vectors.items():
                    if len(self_point_vector.intersection(point_vector)) > 0:
                        overlaps.add(self_point)
        return len(overlaps)


class StarMap():
    def __init__(self, scanners):
        self.scanners = scanners
        self.canonical_positions = {'0': Point(0, 0, 0)}

    def get_all_beacons(self):
        pass


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
    p = Point(0, 7, 8)
    print(p.orientations())

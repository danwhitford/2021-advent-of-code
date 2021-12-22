import os
import itertools


class Cube():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'Cube=({self.x} {self.y} {self.z})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))


class Cuboid():
    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax):
        if xmin > xmax or ymin > ymax or zmin > zmax:
            print(f'err {(xmin, xmax, ymin, ymax, zmin, zmax)}')
            raise "Bad min maxes"
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    def __repr__(self):
        return f'Cuboid=({self.xmin} {self.xmax} {self.ymin} {self.ymax} {self.zmin} {self.zmax})'

    def intersects(self, other):
        return other.xmin <= self.xmax and \
            self.xmin <= other.xmax and \
            other.ymin <= self.ymax and \
            self.ymin <= other.ymax and \
            other.zmin <= self.zmax and \
            self.zmin <= other.zmax

    def split(self, other):
        splits = []

        if other.xmin > self.xmin:
            splits.append(Cuboid(self.xmin, other.xmin-1,
                          self.ymin, self.ymax, self.zmin, self.zmax))
        if other.xmax < self.xmax:
            splits.append(Cuboid(other.xmax+1, self.xmax,
                          self.ymin, self.ymax, self.zmin, self.zmax))

        middle_x_min = max(self.xmin, other.xmin)
        middle_x_max = min(self.xmax, other.xmax)
        if other.ymin > self.ymin:
            splits.append(Cuboid(middle_x_min, middle_x_max,
                          self.ymin, other.ymin-1, self.zmin, self.zmax))
        if other.ymax < self.ymax:
            splits.append(Cuboid(middle_x_min, middle_x_max,
                          other.ymax+1, self.ymax, self.zmin, self.zmax))

        middle_y_min = max(self.ymin, other.ymin)
        middle_y_max = min(self.ymax, other.ymax)
        if other.zmin > self.zmin:
            splits.append(Cuboid(middle_x_min, middle_x_max,
                          middle_y_min, middle_y_max, self.zmin, other.zmin-1))
        if other.zmax < self.zmax:
            splits.append(Cuboid(middle_x_min, middle_x_max,
                          middle_y_min, middle_y_max, other.zmax+1, self.zmax))

        return splits

    def volume(self):
        return (1 + self.xmax - self.xmin) * (1 + self.ymax - self.ymin) * (1 + self.zmax - self.zmin)


class Reactor():
    def __init__(self):
        self.on_cubes = set()
        self.cuboids = []

    def central_reboot(self, instructions):
        self.cuboids = []
        for i in instructions:
            xmin, xmax, ymin, ymax, zmin, zmax = i[1:]
            if xmin < -50 or xmax > 50 or ymin < -50 or ymax > 50 or zmin < -50 or zmax > 50:
                continue
            step = Cuboid(xmin, xmax, ymin, ymax, zmin, zmax)
            new_cuboids = []
            for cuboid in self.cuboids:
                if cuboid.intersects(step):
                    for split in cuboid.split(step):
                        new_cuboids.append(split)
                else:
                    new_cuboids.append(cuboid)
            if i[0] == 'on':
                new_cuboids.append(step)
            self.cuboids = new_cuboids

    def full_reboot(self, instructions):
        self.cuboids = []
        for i in instructions:
            xmin, xmax, ymin, ymax, zmin, zmax = i[1:]
            step = Cuboid(xmin, xmax, ymin, ymax, zmin, zmax)
            new_cuboids = []
            for cuboid in self.cuboids:
                if cuboid.intersects(step):
                    for split in cuboid.split(step):
                        new_cuboids.append(split)
                else:
                    new_cuboids.append(cuboid)
            if i[0] == 'on':
                new_cuboids.append(step)
            self.cuboids = new_cuboids

    def lit_cubes(self):
        total = 0
        for c in self.cuboids:
            total += c.volume()
        return total


class InputParser():
    def __init__(self, s):
        self.lines = s.splitlines()
        self.instructions = []

    def parse(self):
        instructions = []
        for line in self.lines:
            instruction = []
            state, coords = line.split(' ')
            instruction.append(state)
            for coord in coords.split(','):
                coord = coord[2:]
                mi, ma = coord.split('..')
                instruction.append(int(mi))
                instruction.append(int(ma))
            instructions.append(instruction)
        return instructions


if __name__ == '__main__':
    with open(os.path.dirname(__file__) + '/res/day22') as f:
        parser = InputParser(f.read())
        instructions = parser.parse()
        reactor = Reactor()
        reactor.full_reboot(instructions)
        print(reactor.lit_cubes())

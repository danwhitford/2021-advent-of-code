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


class Reactor():
    def __init__(self):
        self.on_cubes = set()

    def make_cuboid(self, xmin, xmax, ymin, ymax, zmin, zmax):
        return {Cube(x,y,z) for x,y,z in itertools.product(range(zmin, zmax+1), range(ymin, ymax+1), range(xmin, xmax+1))}

    def turn_on_cuboid(self, xmin, xmax, ymin, ymax, zmin, zmax):
        print('making')
        cuboid = self.make_cuboid(xmin, xmax, ymin, ymax, zmin, zmax)
        print('doing')
        self.on_cubes.update(cuboid)

    def turn_off_cuboid(self, xmin, xmax, ymin, ymax, zmin, zmax):
        cuboid = self.make_cuboid(xmin, xmax, ymin, ymax, zmin, zmax)
        self.on_cubes.difference_update(cuboid)

    def central_reboot(self, instructions):
        for i in instructions:
            xmin, xmax, ymin, ymax, zmin, zmax = i[1:]
            if xmin < -50 or xmax > 50 or ymin < -50 or ymax > 50: continue
            if i[0] == 'on':
                self.turn_on_cuboid(xmin, xmax, ymin, ymax, zmin, zmax)
            elif i[0] == 'off':
                self.turn_off_cuboid(xmin, xmax, ymin, ymax, zmin, zmax)

    def full_reboot(self, instructions):
        for i in instructions:
            print(i)
            xmin, xmax, ymin, ymax, zmin, zmax = i[1:]
            # if xmin < -50 or xmax > 50 or ymin < -50 or ymax > 50: continue
            if i[0] == 'on':
                self.turn_on_cuboid(xmin, xmax, ymin, ymax, zmin, zmax)
            elif i[0] == 'off':
                self.turn_off_cuboid(xmin, xmax, ymin, ymax, zmin, zmax)


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
        print(len(reactor.on_cubes))

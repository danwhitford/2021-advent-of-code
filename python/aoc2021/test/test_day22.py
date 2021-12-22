import aoc2021.day22 as day22

example_in = '''on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682'''

def test_firststep():
    reactor = day22.Reactor()
    reactor.turn_on_cuboid(10,12,10,12,10,12)
    assert 27 == len(reactor.on_cubes)

def test_secondstep():
    reactor = day22.Reactor()
    reactor.turn_on_cuboid(10,12,10,12,10,12)
    reactor.turn_on_cuboid(11, 13, 11, 13, 11, 13)
    assert 46 == len(reactor.on_cubes)

def test_thirdstep():
    reactor = day22.Reactor()
    reactor.turn_on_cuboid(10,12,10,12,10,12)
    reactor.turn_on_cuboid(11, 13, 11, 13, 11, 13)
    reactor.turn_off_cuboid(9, 11, 9, 11, 9, 11)
    assert 38 == len(reactor.on_cubes)

def test_finalstep():
    reactor = day22.Reactor()
    reactor.turn_on_cuboid(10,12,10,12,10,12)
    reactor.turn_on_cuboid(11, 13, 11, 13, 11, 13)
    reactor.turn_off_cuboid(9, 11, 9, 11, 9, 11)
    reactor.turn_on_cuboid(10, 10, 10, 10, 10, 10)
    assert 39 == len(reactor.on_cubes)

def test_readinput():
    parser = day22.InputParser(example_in)
    instructions = parser.parse()
    assert 22 == len(instructions)
    assert ['on',-20,26,-36,17,-47,7] == instructions[0]
    assert ['off',18,30,-20,-8,-3,13] == instructions[-4]

def test_bigexample():
    parser = day22.InputParser(example_in)
    instructions = parser.parse()
    reactor = day22.Reactor()
    reactor.central_reboot(instructions)
    assert 590784 == len(reactor.on_cubes)

def test_bigbigexample():
    parser = day22.InputParser(example_in)
    instructions = parser.parse()
    reactor = day22.Reactor()
    reactor.full_reboot(instructions)
    assert 2758514936282235 == len(reactor.on_cubes)

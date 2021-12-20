
import aoc2021.day20 as day20
import os

example_in='''..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###'''

def test_readinput0():
    enhancement_algo, initial_image = day20.read_input(example_in)
    assert 512 == len(enhancement_algo)
    assert '#' == enhancement_algo[10]
    assert '.' == enhancement_algo[60]
    assert 10 == len(initial_image)
    assert (0,0) in initial_image
    assert (4,4) in initial_image
    assert (3,0) in initial_image
    assert (3,4) in initial_image

def test_onestep0():
    enhancement_algo, initial_image = day20.read_input(example_in)
    image = day20.enhance_image(initial_image, enhancement_algo)
    day20.print_image(image)
    assert 24 == len(image)

def testtwostep0():
    enhancement_algo, image = day20.read_input(example_in)
    for i in range(2):
        image = day20.enhance_image(image, enhancement_algo)
    day20.print_image(image)
    assert 35 == len(image)

def test_bigexample0():
    with open(os.path.dirname(__file__) + '/../res/day20_example') as f:
        s = f.read()
        algo, image = day20.read_input(s)
        day20.print_image(image)
        print('---')
        for i in range(2):
            image = day20.enhance_image(image, algo, i)
            day20.print_image(image)
            print('---')

        assert 5326 == len(image)

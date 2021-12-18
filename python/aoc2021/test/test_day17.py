import aoc2021.day17 as day17

def test_hits_area1():
    assert day17.hits_area([7, 2], [20, 30, -10, -5])
    assert day17.hits_area([6, 3], [20, 30, -10, -5])
    assert day17.hits_area([9, 0], [20, 30, -10, -5])


def test_not_hit_area1():
    assert not day17.hits_area([17, -4], [20, 30, -10, -5])
    assert not day17.hits_area([6, 10], [20, 30, -10, -5])


def test_highest_y_for_area():
    area = [20, 30, -10, -5]
    assert 45 == day17.highest_y(area)


def test_count_hits1():
    area = [20, 30, -10, -5]
    assert 112 == day17.total_hitting(area)
    
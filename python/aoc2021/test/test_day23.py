import aoc2021.day23 as day23

def test_iscomplete():
    burrow = day23.Burrow((None, None, None, None, None, None, None, None, None, None, None), (('A','A'), ('B','B'), ('C','C'), ('D','D')))
    assert burrow.is_complete()

def test_notcomplete():
    burrow = day23.Burrow((None, None, None, None, None, None, None, None, None, None, None), (('A','B'), ('C','D'),('B', 'C'),('D','A')))
    assert not burrow.is_complete()

def test_compare():
    a = day23.Burrow((None, None, None, None, None, None, None, None, None, None, None), (('A','B'), ('C','D'),('B', 'C'),('D','A')))
    b = day23.Burrow((None, None, None, None, None, None, None, None, None, None, None), (('A','B'), ('C','D'),('B', 'C'),('D','A')))
    assert a == b

def test_hash():
    a = day23.Burrow((None, None, None, None, None, None, None, None, None, None, None), (('A','B'), ('C','D'),('B', 'C'),('D','A')))
    b = day23.Burrow((None, None, None, None, None, None, None, None, None, None, None), (('A','B'), ('C','D'),('B', 'C'),('D','A')))
    assert a.__hash__() == b.__hash__()
    s = {}
    s[a] = 1
    s[b] = 10
    assert 10 == s[a]
    assert 10 == s[b]
    c = day23.Burrow((None, None, None, None, None, None, None, None, None, None, None), (('A','B'), ('C','D'),('B', 'C'),('D','A')))
    assert c in s

# def test_firstexample():
#     burrow = day23.Burrow((None, None, None, None, None, None, None, None, None, None, None), (('A','B'), ('D', 'C'),('C', 'B'),('A', 'D')))
#     example_step = day23.Burrow((None, None, None, 'B', None, None, None, None, None, None, None), (('A','B'), ('D','C'),('C', None),('A', 'D')))
#     assert (example_step, 40) in burrow.get_nextsteps()

# def test_secondexample():
#     burrow = day23.Burrow((None, None, None, 'B', None, None, None, None, None, None, None), (('A','B'), ('D','C'),('C', None),('A', 'D')))
#     example_step = day23.Burrow((None, None, None, 'B', None, None, None, None, None, None, None), (('A','B'), ('D', None), ('C', 'C'),('A', 'D')))
#     assert (example_step, 400) in burrow.get_nextsteps()

# def test_thirdexample():
#     burrow = day23.Burrow((None, None, None, 'B', None, None, None, None, None, None, None), (('A','B'), ('D', None), ('C', 'C'),('A', 'D')))
#     example_step = day23.Burrow((None, None, None, 'B', None, 'D', None, None, None, None, None), (('A','B'), (None, None), ('C', 'C'),('A', 'D')))
#     assert (example_step, 3000) in burrow.get_nextsteps()

# def test_example3andahalf():
#     burrow = day23.Burrow((None, None, None, 'B', None, 'D', None, None, None, None, None), (('A','B'), (None, None), ('C', 'C'),('A', 'D')))
#     example_step = day23.Burrow((None, None, None, None, None, 'D', None, None, None, None, None), (('A','B'), ('B', None), ('C', 'C'),('A', 'D')))
#     assert (example_step, 30) in burrow.get_nextsteps()

# def test_example4():
#     burrow = day23.Burrow((None, None, None, None, None, 'D', None, None, None, None, None), (('A','B'), ('B', None), ('C', 'C'),('A', 'D')))
#     example_step = day23.Burrow((None, None, None, None, None, 'D', None, None, None, None, None), (('A', None), ('B', 'B'), ('C', 'C'),('A', 'D')))
#     assert (example_step, 40) in burrow.get_nextsteps()

# def test_example5():
#     burrow = day23.Burrow((None, None, None, None, None, 'D', None, None, None, None, None), (('A', None), ('B', 'B'), ('C', 'C'),('A', 'D')))
#     example_step = day23.Burrow((None, None, None, None, None, 'D', None, 'D', None, None, None), (('A', None), ('B', 'B'), ('C', 'C'),('A', None)))
#     assert example_step in [b for b, s in burrow.get_nextsteps()]

# def test_example6():
#     burrow = day23.Burrow((None, None, None, None, None, 'D', None, 'D', None, None, None), (('A', None), ('B', 'B'), ('C', 'C'),('A', None)))
#     example_step = day23.Burrow((None, None, None, None, None, 'D', None, 'D', None, 'A', None), (('A', None), ('B', 'B'), ('C', 'C'),(None, None)))
#     assert example_step in [b for b, s in burrow.get_nextsteps()]

# def test_example7():
#     burrow = day23.Burrow((None, None, None, None, None, 'D', None, 'D', None, 'A', None), (('A', None), ('B', 'B'), ('C', 'C'), (None, None)))
#     example_step = day23.Burrow((None, None, None, None, None, 'D', None, None, None, 'A', None), (('A', None), ('B', 'B'), ('C', 'C'),('D', None)))
#     assert example_step in [b for b, s in burrow.get_nextsteps()]

# def test_example8():
#     burrow = day23.Burrow((None, None, None, None, None, 'D', None, None, None, 'A', None), (('A', None), ('B', 'B'), ('C', 'C'),('D', None)))
#     example_step = day23.Burrow((None, None, None, None, None, None, None, None, None, 'A', None), (('A', None), ('B', 'B'), ('C', 'C'),('D', 'D')))
#     assert example_step in [b for b, s in burrow.get_nextsteps()]

def test_final():
    burrow = day23.Burrow((None, None, None, None, None, None, None, None, None, 'A', None), (('A', None), ('B', 'B'), ('C', 'C'),('D', 'D')))
    example_step = day23.Burrow((None, None, None, None, None, None, None, None, None, None, None), (('A', 'A'), ('B', 'B'), ('C', 'C'),('D', 'D')))
    assert example_step in [b for b, s in burrow.get_nextsteps()]
    assert any([b.is_complete() for b, s in burrow.get_nextsteps()])

def test_completebasecase():
    burrow = day23.Burrow((None, None, None, None, None, None, None, None, None, None, None), (('A', 'A'), ('B', 'B'), ('C', 'C'),('D', 'D')))
    assert 0 == len(burrow.get_nextsteps())

def test_cost0():
    burrow = day23.Burrow((None, None, None, None, None, None, None, None, None, 'A', None), (('A', None), ('B', 'B'), ('C', 'C'),('D', 'D')))
    assert 8 == day23.score_to_complete(burrow)

def test_cost1():
    burrow = day23.Burrow((None, None, None, None, None, 'D', None, 'D', None, 'A', None), (('A', None), ('B', 'B'), ('C', 'C'), (None, None)))
    assert 7008 == day23.score_to_complete(burrow)

def test_cost2():
    burrow = day23.Burrow((None, None, None, None, None, 'D', None, None, None, None, None), (('A', None), ('B', 'B'), ('C', 'C'),('A', 'D')))
    assert 9011 == day23.score_to_complete(burrow)

def test_cost3():
    burrow = day23.Burrow((None, None, None, None, None, 'D', None, None, None, None, None), (('A','B'), ('B', None), ('C', 'C'),('A', 'D')))
    assert 9051 == day23.score_to_complete(burrow)

def test_cost4():
    burrow = day23.Burrow((None, None, None, 'B', None, None, None, None, None, None, None), (('A','B'), ('D', None), ('C', 'C'),('A', 'D')))
    assert 12081 == day23.score_to_complete(burrow)

def test_cost5():
    burrow = day23.Burrow((None, None, None, 'B', None, None, None, None, None, None, None), (('A','B'), ('D', 'C'), ('C', None),('A', 'D')))
    assert 12481 == day23.score_to_complete(burrow)

def test_cost6():
    burrow = day23.Burrow((None, None, None, None, None, None, None, None, None, None, None), (('A', 'B'), ('D', 'C'), ('C', 'B'),('A', 'D')))
    assert 12521 == day23.score_to_complete(burrow)

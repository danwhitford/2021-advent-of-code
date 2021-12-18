import aoc2021.day18 as day18


def test_addfish1():
    fish1 = day18.SnailFishParser('[1,2]').getSnailFish()
    fish2 = day18.SnailFishParser('[[3,4],5]').getSnailFish()
    assert ['[','[',1,2,']','[','[',3,4,']',5,']',']'] == day18.add_fish(fish1, fish2)


def test_reduce():
    fish = day18.SnailFishParser('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]').getSnailFish()
    expected = day18.SnailFishParser('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]').getSnailFish()
    assert expected == day18.reduce_fish(fish)


def test_addandreduce0():
    example_in = '''[[[[4,3],4],4],[7,[[8,4],9]]]
        [1,1]'''
    fishes = [day18.SnailFishParser(l.strip()).getSnailFish() for l in example_in.splitlines() if len(l.strip()) > 0]
    expected = day18.SnailFishParser('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]').getSnailFish()
    ret = day18.add_fish_list(fishes)
    assert expected == day18.add_fish_list(fishes)


def test_addandreduce1():
    example_in = '''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
        [[[5,[2,8]],4],[5,[[9,9],0]]]
        [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
        [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
        [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
        [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
        [[[[5,4],[7,7]],8],[[8,3],8]]
        [[9,3],[[9,9],[6,[4,9]]]]
        [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
        [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''
    fishes = [day18.SnailFishParser(l.strip()).getSnailFish() for l in example_in.splitlines() if len(l.strip()) > 0]
    expected = day18.SnailFishParser('[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]').getSnailFish()
    ret = day18.add_fish_list(fishes)
    print(expected)
    print(ret)
    assert expected == day18.add_fish_list(fishes)


def test_addandreduce2():
    ex = '''[1,1]
        [2,2]
        [3,3]
        [4,4]'''
    fishes = [day18.SnailFishParser(l.strip()).getSnailFish() for l in ex.splitlines() if len(l.strip()) > 0]
    expected = day18.SnailFishParser('[[[[1,1],[2,2]],[3,3]],[4,4]]').getSnailFish()
    assert expected == day18.add_fish_list(fishes)


def test_addandreduce3():
    ex = '''[1,1]
        [2,2]
        [3,3]
        [4,4]
        [5,5]'''
    fishes = [day18.SnailFishParser(l.strip()).getSnailFish() for l in ex.splitlines() if len(l.strip()) > 0]
    expected = day18.SnailFishParser('[[[[3,0],[5,3]],[4,4]],[5,5]]').getSnailFish()
    assert expected == day18.add_fish_list(fishes)


def test_addandreduce4():
    ex = '''[1,1]
        [2,2]
        [3,3]
        [4,4]
        [5,5]
        [6,6]'''
    fishes = [day18.SnailFishParser(l.strip()).getSnailFish() for l in ex.splitlines() if len(l.strip()) > 0]
    expected = day18.SnailFishParser('[[[[5,0],[7,4]],[5,5]],[6,6]]').getSnailFish()
    assert expected == day18.add_fish_list(fishes)


    def test_addandreduce5():
        ex = '''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
            [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
            [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
            [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
            [7,[5,[[3,8],[1,4]]]]
            [[2,[2,2]],[8,[8,1]]]
            [2,9]
            [1,[[[9,3],9],[[9,0],[0,7]]]]
            [[[5,[7,4]],7],1]
            [[[[4,2],2],6],[8,7]]'''
        fishes = [day18.SnailFishParser(l.strip()).getSnailFish() for l in ex.splitlines() if len(l.strip()) > 0]
        expected = day18.SnailFishParser('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]').getSnailFish()
        assert expected == day18.add_fish_list(fishes)
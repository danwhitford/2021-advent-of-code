import math

example_in = '''
[1,2]
[[1,2],3]
[9,[8,7]]
[[1,9],[8,5]]
[[[[1,2],[3,4]],[[5,6],[7,8]]],9]
[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]
'''


class SnailFishParser():
    def __init__(self, s):
        self.idx = 0
        self.l = len(s)
        self.s = s

    def reset(self, s):
        self.idx = 0
        self.l = len(s)
        self.s = s

    def getSnailFish(self):
        fish_tokens = []

        while self.idx < self.l:
            n = self.read()
            # print(n)
            if n == '[' or n == ']':
                fish_tokens.append(n)
            elif n == ',':
                continue
            else:
                lexeme = n
                while self.peek().isdigit():
                    lexeme += self.read()
                fish_tokens.append(int(lexeme))

        return fish_tokens

    def peek(self):
        return self.s[self.idx]

    def read(self):
        c = self.s[self.idx]
        self.idx += 1
        return c


def add_fish(fish1, fish2):
    return ['[', *fish1, *fish2, ']']


def reduce_fish(fish):
    idx = 0
    nesting = 0
    while idx < len(fish):
        if nesting != 4 and fish[idx] == '[':
            nesting += 1
        elif fish[idx] == ']':
            nesting -= 1
        elif nesting == 4 and fish[idx] == '[':
            left = fish[idx+1]
            right = fish[idx+2]
            counter = idx-1
            while counter > 0:
                if type(fish[counter]) == int:
                    fish[counter] += left
                    break
                counter -= 1
            counter = idx + 3
            while counter < len(fish):
                if type(fish[counter]) == int:
                    fish[counter] += right
                    break
                counter += 1
            fish = fish[:idx] + [0] + fish[idx+4:]
            idx = 0
            nesting = 0
            continue
        elif fish[idx] >= 10:
            fish = fish[:idx] + \
                ['[', math.floor(fish[idx] / 2),
                 math.ceil(fish[idx] / 2), ']'] + fish[idx+1:]
            idx = 0
            nesting = 0
            continue

        idx += 1

    return fish


def add_fish_list(fishes):
    acc = fishes[0]
    for fish in fishes[1:]:
        added = add_fish(acc, fish)
        acc = reduce_fish(added)
    return acc


if __name__ == '__main__':
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
    fishes = [SnailFishParser(l.strip()).getSnailFish() for l in example_in.splitlines() if len(l.strip()) > 0]
    ret = add_fish_list(fishes)
    print(ret)
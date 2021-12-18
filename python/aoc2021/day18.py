import math
import os 

class SnailFishTokenizer():
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


class SnailFishParser():
    def __init__(self, s):
        self.idx = 0
        self.l = len(s)
        self.s = s


    def getSnailFish(self):
        while self.idx < self.l:
            n = self.read()
            if n == '[':
                left = self.getSnailFish()
                right = self.getSnailFish()
                assert ']' == self.read()
                return {
                    'left': left,
                    'right': right,
                }
            else:
                assert type(n) == int
                return n


    def peek(self):
        return self.s[self.idx]

    def read(self):
        c = self.s[self.idx]
        self.idx += 1
        return c


def add_fish(fish1, fish2):
    return ['[', *fish1, *fish2, ']']


def explode(fish):
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
            return fish, True
        idx += 1
    return fish, False


def split(fish):
    idx = 0
    while idx < len(fish):
        if type(fish[idx]) == int and fish[idx] >= 10:
            fish = fish[:idx] + \
                ['[', math.floor(fish[idx] / 2),
                 math.ceil(fish[idx] / 2), ']'] + fish[idx+1:]
            return fish, True
        idx += 1
    return fish, False


def reduce_fish(fish):
    while True:
        fish, c1 = explode(fish)
        if c1:
            continue
        fish, c2 = split(fish)  
        if not c1 and not c2:
            break
    return fish


def add_fish_list(fishes):
    acc = fishes[0]
    for fish in fishes[1:]:
        added = add_fish(acc, fish)
        acc = reduce_fish(added)
    return acc


def magnitude(fish):
    fish_tree = SnailFishParser(fish).getSnailFish()
    def inner(fish):
        if type(fish) == dict:
            return (inner(fish['left']) * 3)  + (inner(fish['right']) * 2)
        else:
            return fish
    return inner(fish_tree)


def find_largest_magnitude(fishes):
    m = 0
    for i in fishes:
        for j in fishes:
            if i == j: continue
            res = add_fish_list([i, j])
            res = magnitude(res)
            if res > m:
                m = res
    return m


if __name__ == '__main__':
    with open(os.path.dirname(__file__) + '/res/day18') as f:
        s = f.read()
        fishes = [SnailFishTokenizer(l.strip()).getSnailFish() for l in s.splitlines() if len(l.strip()) > 0]
        print(find_largest_magnitude(fishes))

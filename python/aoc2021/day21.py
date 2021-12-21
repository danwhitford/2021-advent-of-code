import itertools


class Game():
    def __init__(self, player_one_pos, player_two_pos, next_roll, p1_score, p2_score):
        self.p1_pos = player_one_pos
        self.p2_pos = player_two_pos
        self.p1_score = p1_score
        self.p2_score = p2_score
        self.next_roll = next_roll

    def move(self, p):
        points = sum(self.next_roll)
        if p == 1:
            self.p1_pos += points
            if self.p1_pos > 10:
                self.p1_pos = (self.p1_pos - 1) % 10 + 1
            self.p1_score += self.p1_pos
        else:
            self.p2_pos += points
            if self.p2_pos > 10:
                self.p2_pos = (self.p2_pos - 1) % 10 + 1
            self.p2_score += self.p2_pos


def rolls():
    return itertools.product([1, 2, 3], repeat=3)


def play(p1start, p2start):
    stack = []

    for universe in rolls():
        stack.append(Game(p1start, p2start, universe, 0, 0))

    wins = {'p1': 0, 'p2': 0}
    while len(stack) > 0:
        print(wins)

        game = stack.pop()

        game.move(1)
        if game.p1_score >= 21:
            wins['p1'] += 1
            continue
        game.move(2)
        if game.p2_score >= 21:
            wins['p2'] += 1
            continue

        # game not finished
        # stack.append(game)
        for universe in rolls():
            stack.append(Game(game.p1_pos, game.p2_pos,
                         universe, game.p1_score, game.p2_score))
    return wins


if __name__ == '__main__':
    res = play(4, 8)
    # print(f'Rolls: {game.rolls} P1: {game.p1_score} P2: {game.p2_score}')
    print(res)

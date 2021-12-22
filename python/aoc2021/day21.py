import itertools
import functools


class GameState():
    def __init__(self, p1pos, p2pos, p1score, p2score, nextroll, nextplayer):
        self.p1pos = p1pos
        self.p2pos = p2pos
        self.p1score = p1score
        self.p2score = p2score
        self.nextroll = nextroll
        self.nextplayer = nextplayer

    def __repr__(self):
        return f'{self.p1pos} {self.p2pos} {self.p1score} {self.p2score} {self.nextroll} {self.nextplayer}'

    def __eq__(self, other):
        return self.p1pos == other.p1pos and self.p2pos == other.p2pos and self.p1score == other.p1score and self.p2score == other.p2score and self.nextroll == other.nextroll and self.nextplayer == other.nextplayer

    def __hash__(self):
        return hash((self.p1pos, self.p2pos, self.p1score,
                     self.p2score, self.nextroll, self.nextplayer))

# @functools.cache
def move(gamestate):
    points = sum(gamestate.nextroll)
    p1pos = gamestate.p1pos
    p1score = gamestate.p1score
    p2pos = gamestate.p2pos
    p2score = gamestate.p2score
    if gamestate.nextplayer == 1:
        p1pos = gamestate.p1pos + points
        if p1pos > 10:
            p1pos = (p1pos - 1) % 10 + 1
        p1score = gamestate.p1score + p1pos
    else:
        p2pos = gamestate.p2pos + points
        if p2pos > 10:
            p2pos = (p2pos - 1) % 10 + 1
        p2score = gamestate.p2score + p2pos
    nextplayer = 1 if gamestate.nextplayer == 2 else 2
    return GameState(p1pos, p2pos, p1score, p2score, gamestate.nextroll, nextplayer)


def rolls():
    return itertools.product([1, 2, 3], repeat=3)


def play(p1start, p2start):
    metaverse = {}
    for universe in rolls():
        metaverse[GameState(p1start, p2start, 0, 0, universe, 1)] = 1

    wins = [0, 0]
    counter = 0
    while len(metaverse) > 0:
        if counter > 1000000:
            print(wins)
            counter = 0
        counter += 1

        # new_metaverse = {}
        game, game_count = metaverse.popitem()
        next_game = move(game)

        if next_game.p1score >= 21:
            wins[0] += 1
            continue
        if next_game.p2score >= 21:
            wins[1] += 1
            continue

        for universe in rolls():
            next_game = GameState(next_game.p1pos, next_game.p2pos,
                                  next_game.p1score, next_game.p2score, universe, next_game.nextplayer)
            if next_game in metaverse:
                metaverse[next_game] += game_count
            else:
                metaverse[next_game] = game_count

    return wins


if __name__ == '__main__':
    res = play(4, 8)
    print(res)

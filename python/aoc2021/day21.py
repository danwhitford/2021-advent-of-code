import itertools
import collections
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
        return f'GameState=({self.p1pos} {self.p2pos} {self.p1score} {self.p2score} {self.nextroll} {self.nextplayer})'

    def __eq__(self, other):
        return self.p1pos == other.p1pos and self.p2pos == other.p2pos and self.p1score == other.p1score and self.p2score == other.p2score and self.nextroll == other.nextroll and self.nextplayer == other.nextplayer

    def __hash__(self):
        return hash((self.p1pos, self.p2pos, self.p1score,
                     self.p2score, self.nextroll, self.nextplayer))

def next_step(pos, score, points):
    pos = pos + points
    if pos > 10:
        pos = (pos - 1) % 10 + 1
    return pos, score + pos

@functools.cache
def move(gamestate):
    points = gamestate.nextroll

    p1pos = gamestate.p1pos
    p1score = gamestate.p1score
    p2pos = gamestate.p2pos
    p2score = gamestate.p2score

    if gamestate.nextplayer == 1:
        p1pos, p1score = next_step(p1pos, p1score, points)
    else:
        p2pos, p2score = next_step(p2pos, p2score, points)

    nextplayer = 1 if gamestate.nextplayer == 2 else 2
    return GameState(p1pos, p2pos, p1score, p2score, gamestate.nextroll, nextplayer)


def rolls():
    return itertools.product([1, 2, 3], repeat=3)


def play(p1start, p2start):
    metaverse = collections.OrderedDict()
    for universe in rolls():
        metaverse[GameState(p1start, p2start, 0, 0, sum(universe), 1)] = 1

    wins = [0, 0]
    counter = 0
    while len(metaverse) > 0:
        if counter > 100000:
            print(wins, len(metaverse))
            print(move.cache_info())
            counter = 0
        counter += 1

        game, game_count = metaverse.popitem()
        next_game = move(game)

        if next_game.p1score >= 21:
            wins[0] += game_count
            continue
        if next_game.p2score >= 21:
            wins[1] += game_count
            continue

        for universe in rolls():
            ng = GameState(next_game.p1pos, next_game.p2pos,
                                  next_game.p1score, next_game.p2score, sum(universe), next_game.nextplayer)
            if ng in metaverse:
                metaverse[ng] += game_count
            else:
                metaverse[ng] = game_count

    return wins


if __name__ == '__main__':
    res = play(4, 8)
    print(res)

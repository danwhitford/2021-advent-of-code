import itertools
import functools

@functools.lru_cache(maxsize=None)
def move(p1_pos, p2_pos, next_roll, p1_score, p2_score, next_player):
    points = sum(next_roll)
    if next_player == 1:
        p1_pos += points
        if p1_pos > 10:
            p1_pos = (p1_pos - 1) % 10 + 1
        p1_score += p1_pos
    else:
        p2_pos += points
        if p2_pos > 10:
            p2_pos = (p2_pos - 1) % 10 + 1
        p2_score += p2_pos
    next_player = 1 if next_player == 2 else 2
    return (p1_pos, p2_pos, p1_score, p2_score, next_player)


def rolls():
    return itertools.product([1, 2, 3], repeat=3)


def play(p1start, p2start):
    stack = []

    for universe in rolls():
        stack.append((p1start, p2start, universe, 0, 0, 1))

    wins = {'p1': 0, 'p2': 0}
    counter = 0
    while len(stack) > 0:
        counter += 1
        if counter % 10000 == 0:
            print(wins)
        
        p1_pos, p2_pos, universe, p1_score, p2_score, next_player = stack.pop()

        p1_pos, p2_pos, p1_score, p2_score, next_player = move(p1_pos, p2_pos, universe, p1_score, p2_score, next_player)
        if p1_score >= 21:
            wins['p1'] += 1
            continue

        for universe in rolls():            
            stack.append((p1_pos, p2_pos, universe, p1_score, p2_score, next_player))

        p1_pos, p2_pos, p1_score, p2_score, next_player = move(p1_pos, p2_pos, universe, p1_score, p2_score, next_player)
        if p2_score >= 21:
            wins['p2'] += 1
            continue

        for universe in rolls():            
            stack.append((p1_pos, p2_pos, universe, p1_score, p2_score, next_player))
    print(counter)
    return wins


if __name__ == '__main__':
    res = play(4, 8)
    # print(f'Rolls: {game.rolls} P1: {game.p1_score} P2: {game.p2_score}')
    print(res)

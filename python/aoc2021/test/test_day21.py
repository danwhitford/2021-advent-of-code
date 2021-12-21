import aoc2021.day21 as day21

example_input = '''Player 1 starting position: 4
Player 2 starting position: 8'''

def test_example():
    game = day21.Game(4, 8)
    print(game.play())
    
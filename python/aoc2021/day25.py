import os

example_in = '''v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>'''

def make_grid(s):
    return [list(line) for line in s.split('\n') if len(line.strip()) > 0]

def take_step(grid):
    moved = False
    new_grid = [list(line) for line in grid]

    for y, line in enumerate(grid):
        for x, cell in enumerate(line):
            if cell != '>':
                continue
            next_cell = grid[y][x+1] if x < len(line) - 1 else grid[y][0]
            if next_cell == '.':
                moved = True
                new_grid[y][x] = '.'
                if x < len(line) - 1:
                    new_grid[y][x+1] = '>'
                else:
                    new_grid[y][0] = '>'

    grid = new_grid
    new_grid = [list(line) for line in grid]

    for y, line in enumerate(grid):
        for x, cell in enumerate(line):
            if cell != 'v':
                continue
            next_cell = grid[y+1][x] if y < len(grid) - 1 else grid[0][x]
            if next_cell == '.':
                moved = True
                new_grid[y][x] = '.'
                if y < len(grid) - 1:
                    new_grid[y+1][x] = 'v'
                else:
                    new_grid[0][x] = 'v'
    
    return (new_grid, moved)       


def print_grid(grid):
    for line in grid:
        print(''.join(line))
    print('')


if __name__ == '__main__':
    with open(os.path.dirname(__file__) + '/res/day25') as f:
        count = 0
        g = make_grid(f.read())
        while True:
            count += 1
            g, moved = take_step(g)
            print(count)
            print_grid(g)
            if not moved:
                break
    print(f'Count is {count}')
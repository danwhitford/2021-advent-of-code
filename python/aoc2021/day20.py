import os


def read_input(s):
    algo = s.splitlines()[0].strip()
    
    lights = set()
    grid = s.splitlines()[2:]
    for y, row in enumerate(grid):
        for x, light in enumerate(row):
            if light == '#':
                lights.add((x,y))

    return algo, lights


def enhance_image(image, algo, step=None):
    new_image = set()
    min_x = min([p[0] for p in image])
    max_x = max([p[0] for p in image])
    min_y = min([p[1] for p in image])
    max_y = max([p[1] for p in image])
    for x in range(min_x-1, max_x+2):
        for y in range(min_y-1, max_y+2):
            if (algo[0] == '#' and algo[-1] == '.') and (x < min_x or x > max_x or y < min_y or y > max_y):
                if step % 2 == 0:
                    new_image.add((x, y))
            else:
                neighbours = [
                    (x-1,y-1),
                    (x, y-1),
                    (x+1,y-1),
                    (x-1,y),
                    (x,y),
                    (x+1,y),
                    (x-1,y+1),
                    (x,y+1),
                    (x+1,y+1)
                ]
                neighbour_string = ''
                for xx, yy in neighbours:
                    if (not step) or (min_x <= xx <= max_x and min_y <= yy <= max_y):
                        neighbour_string += '1' if (xx, yy) in image else '0'
                    else:
                        neighbour_string += '0' if step % 2 == 0 else '1'
                neighbour_num = int(neighbour_string, 2)
                if algo[neighbour_num] == '#':
                    new_image.add((x,y))
    return new_image


def print_image(image):
    min_x = min([p[0] for p in image])
    max_x = max([p[0] for p in image])
    min_y = min([p[1] for p in image])
    max_y = max([p[1] for p in image])
    for x in range(min_x, max_x+1):
        row = ''
        for y in range(min_y, max_y+1):
            row += '#' if (x, y) in image else '.'
        print(row)


if __name__ == '__main__':
    with open(os.path.dirname(__file__) + '/res/day20') as f:
        s = f.read()
        algo, image = read_input(s)
        print_image(image)
        print('---')
        for i in range(2):
            image = enhance_image(image, algo, i)
            print_image(image)
            print('---')

        print(len(image))

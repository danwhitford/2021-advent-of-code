
def step(pos, vel):
    x, y = pos
    xvel, yvel = vel
    x += xvel
    y += yvel
    if xvel > 0:
        xvel -= 1
    elif xvel <0:
        xvel += 1
    yvel -= 1
    return [x,y], [xvel,yvel]
    

def in_box(pos, box):
    x, y = pos
    xmin, xmax, ymin, ymax = box
    return x >= xmin and x <= xmax and y >= ymin and y <= ymax
    

def missed_box(pos, box):
    x, y = pos
    xmin, xmax, ymin, ymax = box
    return x > xmax or y < ymin


def hits_area(vel, area):
    pos = [0,0]
    while True:
        pos, vel = step(pos, vel)
        
        if in_box(pos, area):
            return True

        if missed_box(pos, area):
            return False


def get_highest_y_for_vel(y):
    return (y * (y + 1)) / 2


def highest_y(area):
    _, xmax, ymin, _ = area
    candidate_y = 0
    for x in range(1, xmax+1):
        for y in range (ymin, abs(ymin)):
            vel = [x, y]
            if hits_area(vel, area):
                candidate_y = y if y > candidate_y else candidate_y
    return get_highest_y_for_vel(candidate_y)


def total_hitting(area):
    _, xmax, ymin, _ = area
    hitting = 0
    for x in range(1, xmax+1):
        for y in range (ymin, abs(ymin)):
            vel = [x, y]
            if hits_area(vel, area):
                hitting += 1
    return hitting


if __name__ == '__main__':
    print(total_hitting([96, 125, -144, -98]))

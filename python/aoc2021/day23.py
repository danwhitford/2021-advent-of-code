
from typing import Tuple, Literal, Optional
from dataclasses import dataclass
import functools
import heapq

AMPHIPOD = Literal['A', 'B', 'C', 'D']
SQUARE = Optional[AMPHIPOD]

#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########


costs = {
  'A': 1,
  'B': 10,
  'C': 100,
  'D': 1000,
}

room_pos = {
  0: 2,
  1: 4,
  2: 6,
  3: 8,
}

target_room = {
  'A': 0,
  'B': 1,
  'C': 2,
  'D': 3,
}

@dataclass(frozen=True)
class Burrow():
    hall: Tuple[SQUARE, SQUARE, SQUARE, SQUARE, SQUARE,
                SQUARE, SQUARE, SQUARE, SQUARE, SQUARE, SQUARE]
    rooms: Tuple[Tuple[SQUARE, SQUARE], Tuple[SQUARE, SQUARE],
                 Tuple[SQUARE, SQUARE], Tuple[SQUARE, SQUARE], ]

    def __repr__(self):
      s = "#############\n"
      s += '#'
      for r in self.hall:
        s += r if r != None else '.'
      s += '#\n'
      s += '###'
      for r in [a[1] for a in self.rooms]:
        s += r if r is not None else '.'
        s += '#'
      s += '##\n'
      s += '  #'
      for r in [a[0] for a in self.rooms]:
        s += r if r is not None else '.'
        s += '#'
      s += '  \n'
      s += '  #########  \n\n'
      return s

    def is_complete(self):
      things = 0
      for h in self.hall:
        if h is not None:
          things += 1
      for r in self.rooms:
        if r[0] is not None:
          things += 1
        if r[1] is not None:
          things += 1
      if things != 8:
        print(self)
        raise 'Youve lost some things'
      return self.rooms == (('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'))

    def get_nextsteps(self):
        nextsteps = []

        # Move hall to room
        for square_num, square in enumerate(self.hall):
          for room_num, room in enumerate(self.rooms):
            if square is not None and self.can_move(square_num, room_pos[room_num]) and self.has_space(room) and room_num == target_room[square]:
                if room[0] is not None and room_num != target_room[room[0]]: continue
                if room[1] is not None and room[1] != target_room[room[1]]: continue

                new_halls = list(self.hall)
                new_rooms = list(self.rooms)
                new_room = list(self.rooms[room_num])

                new_halls[square_num] = None
                if new_room[0] == None:
                  new_room[0] = square
                else:
                  new_room[1] = square
                new_rooms[room_num] = tuple(new_room)

                cost = abs(square_num - room_pos[room_num])
                cost += 1 if new_room[1] == square else 2
                cost *= costs[square]

                nextsteps.append((Burrow(tuple(new_halls), tuple(new_rooms)), cost))

        # Move room to hall
        for room_num, room in enumerate(self.rooms):
            is_top = False if room[1] is None else True
            top = room[1] if is_top else room[0]

            if top is None: continue
            if (room_num == target_room[room[0]] and room[1] == None) or (room_num == target_room[room[0]] and room_num == target_room[room[1]]):
              continue

            for square_num, square in enumerate(self.hall):
                if square is None and square_num not in [2, 4, 6, 8] and self.can_move(room_pos[room_num], square_num):
                    new_halls = list(self.hall)
                    new_rooms = list(self.rooms)
                    new_room = list(self.rooms[room_num])

                    new_halls[square_num] = top
                    if is_top:
                      new_room[1] = None
                    else:
                      new_room[0] = None
                    new_rooms[room_num] = tuple(new_room)

                    cost = abs(room_pos[room_num] - square_num)
                    cost += (1 if is_top else 2)
                    cost *= costs[top]
                    nextsteps.append((Burrow(tuple(new_halls), tuple(new_rooms)), cost))



        # Move room to room
        # for room_num, room in enumerate(self.rooms):
        #   for to_room_num, to_room in enumerate(self.rooms):
        #     if room_num == to_room_num: continue
            
        #     is_top = False if room[1] is None else True
        #     top = room[1] if is_top else room[0]
        #     if top is None: continue

        #     if target_room[top] == to_room_num and self.can_move(room_pos[room_num], room_pos[to_room_num]) and self.has_space(to_room):
        #         new_halls = list(self.hall)
        #         new_rooms = list(self.rooms)
        #         new_room = list(self.rooms[room_num])
        #         new_to_room = list(self.rooms[to_room_num])

        #         if is_top:
        #           new_room[1] = None
        #         else:
        #           new_room[0] = None
        #         new_rooms[room_num] = tuple(new_room)

        #         if to_room[0] == None:
        #           new_to_room[0] = top
        #         else:
        #           new_to_room[1] = top
        #         new_rooms[to_room_num] = tuple(new_to_room)
              
        #         cost = abs(room_pos[room_num] - room_pos[to_room_num])
        #         cost += 1 if is_top else 2
        #         cost += 1 if new_to_room[1] == top else 2
        #         cost *= costs[top]

        #         nextsteps.append((Burrow(tuple(new_halls), tuple(new_rooms)), cost))
        return nextsteps

    def can_move(self, from_sq, to_sq):
        if from_sq < to_sq:
            return all([s is None for s in self.hall[from_sq+1:to_sq+1]])
        else:
            return all([s is None for s in self.hall[to_sq+1:from_sq]])

    def has_space(self, room):
      return room[0] is None or room[1] is None


def score_to_complete(burrow):
    scores = {
      burrow: 0
    }
    visited = set()
    unvisited = []
    heapq.heappush(unvisited, (0, 0, burrow))

    count = 0
    while len(unvisited) > 0:
      if count % 10000 == 0:
        print(f'unvis {len(unvisited):,}')
      oldscore, _, b = heapq.heappop(unvisited)
      b.is_complete()
      visited.add(b)

      for neighbour, score in b.get_nextsteps():
        if neighbour in visited: continue

        if neighbour in scores:
          if oldscore + score < scores[neighbour]:
            scores[neighbour] = oldscore + score
        else:
          scores[neighbour] = oldscore + score

        count += 1
        heapq.heappush(unvisited, (scores[neighbour], count, neighbour))


    for k, v in scores.items():
      if k.is_complete():
        print(k)
        print('Answer', v)
        return v


if __name__ == '__main__':
    burrow = Burrow((None, None, None, None, None, None, None, None, None, None, None), (('C', 'A'), ('D', 'D'), ('B', 'A'),('B', 'C')))
    print(burrow)
    score_to_complete(burrow)
  

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
      h = max(len(r) for r in self.rooms)
      s = "#############\n"
      s += '#'
      for r in self.hall:
        s += r if r != None else '.'
      s += '#\n'
      s += '###'
      for r in [a[h-1] for a in self.rooms]:
        s += r if r is not None else '.'
        s += '#'
      s += '##\n'
      for i in range(h-2, 0-1, -1):
        s += '  #'
        for r in [a[i] for a in self.rooms]:
          s += r if r is not None else '.'
          s += '#'
        s += '  \n'
      s += '  #########  \n\n'
      return s

    def is_complete(self):
      for i, c in enumerate(['A','B','C','D']):
        if any(c != l for l in self.rooms[i]):
          return False
      return True

    def get_nextsteps(self):
        nextsteps = []

        # Move hall to room
        for square_num, square in enumerate(self.hall):
          for room_num, room in enumerate(self.rooms):
            if square is not None and self.can_move(square_num, room_pos[room_num]) and self.has_space(room) and room_num == target_room[square]:
                if any([room_num != target_room[r] for r in room if r is not None]): continue

                new_halls = list(self.hall)
                new_rooms = list(self.rooms)
                new_room = list(self.rooms[room_num])

                new_halls[square_num] = None
                first_empty = 0
                for i,r in enumerate(room):
                  if r is None:
                    first_empty = i
                    break
                new_room[first_empty] = square
                new_rooms[room_num] = tuple(new_room)

                cost = abs(square_num - room_pos[room_num])
                cost += len(room) - first_empty
                cost *= costs[square]

                nextsteps.append((Burrow(tuple(new_halls), tuple(new_rooms)), cost))

        if len(nextsteps) > 0:
          return nextsteps

        # Move room to hall
        for room_num, room in enumerate(self.rooms):
            is_top = room[len(room)-1] is not None
            top = None
            top_pos = None
            for i, r in enumerate(room):
              if r is not None:
                top = r
                top_pos = i
            if top is None: continue

            if all(room_num == target_room[r] for r in room if r is not None):
              continue

            for square_num, square in enumerate(self.hall):
                if square is None and square_num not in [2, 4, 6, 8] and self.can_move(room_pos[room_num], square_num):
                    new_halls = list(self.hall)
                    new_rooms = list(self.rooms)
                    new_room = list(self.rooms[room_num])

                    new_halls[square_num] = top
                    new_room[top_pos] = None
                    new_rooms[room_num] = tuple(new_room)

                    cost = abs(room_pos[room_num] - square_num)
                    cost += len(room) - top_pos
                    cost *= costs[top]
                    nextsteps.append((Burrow(tuple(new_halls), tuple(new_rooms)), cost))

        return nextsteps

    def can_move(self, from_sq, to_sq):
        if from_sq < to_sq:
            return all([s is None for s in self.hall[from_sq+1:to_sq+1]])
        else:
            return all([s is None for s in self.hall[to_sq+1:from_sq]])

    def has_space(self, room):
      return any(r is None for r in room)


def h(burrow):
  ins = 1
  outs = 1
  for h in burrow.hall:
    if h is None:
      outs += 1
    else:
      ins += 1
  perc_in = ins / (len(burrow.hall) + 1)
  return 2 * perc_in


def score_to_complete(burrow):
    g_scores = {
      burrow: 0
    }
    visited = set()
    unvisited = []
    previous = {}
    heapq.heappush(unvisited, (0, 0, burrow))

    count = 0
    while len(unvisited) > 0:
      oldscore, _, b = heapq.heappop(unvisited)

      if b.is_complete():
        return g_scores[b]

      for neighbour, dist in b.get_nextsteps():
        tento_score = g_scores[b] + dist
        neighbour_gscore = g_scores.get(neighbour, float('inf'))
        if tento_score < neighbour_gscore:
          previous[neighbour] = b
          g_scores[neighbour] = tento_score
          count += 1
          heapq.heappush(unvisited, (tento_score + h(neighbour), count, neighbour))

    raise "poop"

if __name__ == '__main__':
    # burrow = Burrow((None, None, None, None, None, None, None, None, None, None, None), (('C', 'A'), ('D', 'D'), ('B', 'A'),('B', 'C')))
    burrow = Burrow((None, None, None, None, None, None, None, None, None, None, None), (('C', 'D', 'D', 'A'), ('D', 'B', 'C', 'D'), ('B', 'A', 'B', 'A'),('B', 'C', 'A', 'C')))
    print(burrow)
    print(score_to_complete(burrow))
  
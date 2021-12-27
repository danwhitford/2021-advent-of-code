import os
import itertools
import sys
import heapq
class ALU():
    def __init__(self):
        self.environment = {
            'w': 0,
            'x': 0,
            'y': 0,
            'z': 0,
        }

    def reset(self):
        self.environment = {
            'w': 0,
            'x': 0,
            'y': 0,
            'z': 0,
        }

    def read_program(s):
        return [l.strip().split(' ') for l in s.split('\n') if len(l.strip()) > 0]

    def load_program(self, s):
        self.instructions = ALU.read_program(s)

    def execute(self, input_buffer):
        for n, i in enumerate(self.instructions):
            cmd = i[0]
            if cmd == 'inp':        
                self.environment[i[1]] = int(input_buffer.pop(0))
                continue

            lt = self.environment[i[1]]
            rt = self.environment.get(i[2]) if i[2] in self.environment else int(i[2])        

            if cmd == 'add':
                self.environment[i[1]] = lt + rt
            elif cmd == 'mul':
                self.environment[i[1]] = lt * rt
            elif cmd == 'div':
                self.environment[i[1]] = lt // rt
            elif cmd == 'mod':
                self.environment[i[1]] = lt % rt
            elif cmd == 'eql':
                self.environment[i[1]] = 1 if lt == rt else 0
            else:
                raise Exception("uwotm8")


    def validate_model_number(self, mn):
        self.reset()
        self.execute(list(mn))            
        return self.environment['z'] == 0


if __name__ == '__main__':
    alu = ALU()
    with open(os.path.dirname(__file__) + '/res/day24') as f:
        alu.load_program(f.read())

    pq = []
    visited = set()
    start = (9,9,9,9,9,9,9,9,9,9,9,9,9,9)
    alu.validate_model_number(start)
    heapq.heappush(pq, (alu.environment['z'], 0, start))
    visited.add(start)

    count = 0
    while len(pq) > 0:
        score, _, mn = heapq.heappop(pq)
        visited.add(mn)

        if count % 10000 == 0:
            print(f'Queue: {len(pq):,}')
            print(f'Visited: {len(visited):,}')
            print(f'Current {mn}')

        if score == 0:
            print('wow')
            print(mn)
            break

        for n in range(14):            
            neighbour = list(mn)
            neighbour[n] -= 1
            if tuple(neighbour) in visited:
                continue
            alu.validate_model_number(neighbour)
            count += 1
            heapq.heappush(pq, (alu.environment['z'], count, tuple(neighbour)))
    
 
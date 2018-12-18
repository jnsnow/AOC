import itertools
import logging

class Simulation:
    def __init__(self, filename):
        self.state = []
        f = open(filename, 'r')
        for line in f:
            self.state.append(list(line.strip()))
        self.initial = self.copy()

    def copy(self):
        new = []
        for row in self.state:
            new.append(row.copy())
        return new

    def reset(self):
        self.state = self.initial
        self.initial = self.copy()

    def tile(self, x, y):
        if x < 0 or y < 0:
            return ' '
        try:
            return self.state[y][x]
        except IndexError:
            return ' '

    def score(self):
        lumber = 0
        woods = 0
        for row in self.state:
            lumber += len([c for c in row if c == '#'])
            woods += len([c for c in row if c == '|'])
        return lumber * woods

    def print(self):
        for row in self.state:
            print(''.join(row))

    def __hash__(self):
        chars = []
        for row in self.state:
            chars.append(''.join(row))
        return hash(''.join(chars))

    def iterate(self):
        nstate = self.copy()
        for y in range(len(self.state)):
            for x in range(len(self.state[y])):
                cell = self.tile(x, y)
                ring = [self.tile(x_,y_) for x_, y_ in
                        itertools.product([x-1, x, x+1], [y-1, y, y+1])
                        if (x_, y_) != (x, y)]
                if cell == '.' and len([c for c in ring if c == '|']) >= 3:
                    nstate[y][x] = '|'
                elif cell == '|' and len([c for c in ring if c == '#']) >= 3:
                    nstate[y][x] = '#'
                elif cell == '#':
                    if ('#' in ring) and ('|' in ring):
                        nstate[y][x] = '#'
                    else:
                        nstate[y][x] = '.'
        self.state = nstate


def aoc18(filename, p1minutes=10, p2minutes=1000000000):
    sim = Simulation(filename)

    hashes = {}
    history = [hash(sim)]
    sequence = []

    for generation in range(1, p2minutes + 1):
        logging.debug("%003d" % generation)
        sim.iterate()
        hval = hash(sim)
        history.append(hval)

        # This board hasn't been seen before
        if hval not in hashes:
            score = sim.score()
            hashes[hval] = score
            sequence = []
            continue

        # This board HAS been seen
        if not sequence:
            start = history.index(hval)
        sequence.append(hval)
        if history[start:start + len(sequence)] != sequence:
            sequence = []
        if history[start] == sequence[-1]:
            # This board is the same as the start of our tentative sequence
            cycle = len(sequence) - 1
            if not cycle or cycle % 2:
                continue
            # Sequence has already doubled, confirming the minimal loop
            if sequence[:int(cycle/2)] == sequence[int(cycle/2):-1]:
                loop = sequence[:int(cycle/2)].copy()
                assert(loop == history[start:start+len(loop)])
                logging.debug("loop: %s", str(loop))
                logging.debug("found sequence loop [%d:%d]!", start, start+len(loop))
                logging.debug("loop is length %d", len(loop))
                break

    # If the loop broke early, use the cycle data
    if generation != p2minutes:
        p2answ = hashes[loop[(p2minutes - start) % len(loop)]]
    else:
        # lol
        p2answ = hashes[hval]

    return [hashes[history[p1minutes]], p2answ]

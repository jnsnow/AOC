from collections import defaultdict
from dataclasses import dataclass

@dataclass
class rule:
    pattern: str
    result: str
    def __init__(self, raw):
        tmp = raw.split(' => ')
        self.pattern = tmp[0]
        self.result = tmp[1].strip()

class simulation:
    def __init__(self, state, rules):
        # find rules that produce a plant, the others are safe to ignore
        self.rules = [r for r in rules if r.result == '#']
        # Implement as a sparse dict, as is tradition
        self.state = defaultdict(lambda: '.')
        for i in range(len(state)):
            self.state[i] = state[i]

    def tick(self):
        # Rules need a lookback/lookahead of +-2
        low = min(self.state.keys()) - 2
        high = max(self.state.keys()) + 2
        nextgen = defaultdict(lambda: '.')
        for k in range(low, high + 1):
            for r in self.rules:
                if (self.state[k-2] == r.pattern[0] and
                    self.state[k-1] == r.pattern[1] and
                    self.state[k] == r.pattern[2] and
                    self.state[k+1] == r.pattern[3] and
                    self.state[k+2] == r.pattern[4]):
                        nextgen[k] = '#'
        self.state = nextgen

    def value(self):
        return sum(self.state.keys())

def load(filename):
    f = open(filename, "r")
    line = f.readline()
    state = line.split('initial state:' )[1].strip()
    _ = f.readline()
    rules = [rule(line) for line in f]
    return (state, rules)

def p1(state, rules):
    sim = simulation(state, rules)
    for generation in range(1, 20 + 1):
        sim.tick()
    return sim.value()

def p2(state, rules, cycles=50000000000):
    # This really feels like cheating because I can't guarantee it produces a correct result,
    # but it does definitely produce a result which was correct for me, so...
    #
    # ¯\_(ツ)_/¯
    #
    sim = simulation(state, rules)
    last = sim.value()
    lastdiff = 0
    for generation in range(1, cycles + 1):
        sim.tick()
        current = sim.value()
        difference = current - last
        if difference == lastdiff:
            # The simulation begins to cycle here, mercifully
            break
        last = current
        lastdiff = difference
    remaining = cycles - generation
    return current + (remaining * difference)

def aoc12(filename):
    state, rules = load(filename)
    return [p1(state, rules),
            p2(state, rules)]

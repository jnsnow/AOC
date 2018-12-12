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

def load(filename):
    f = open("/home/nago/Documents/input12.txt", "r")
    line = f.readline()
    state = line.split('initial state:' )[1].strip()
    _ = f.readline()
    rules = [rule(line) for line in f]
    return (state, rules)

def p1(state, rules):
    # find rules that produce a plant, the others are safe to ignore
    prodrules = [r for r in rules if r.result == '#']

    # Implement as a sparse dict, as is tradition
    sim = defaultdict(lambda: '.')
    for i in range(len(state)):
        sim[i] = state[i]

    for generation in range(1, 20 + 1):
        # Rules need a lookback/lookahead of +-2
        low = min(sim.keys()) - 2
        high = max(sim.keys()) + 2
        nextgen = defaultdict(lambda: '.')
        for k in range(low, high + 1):
            for r in prodrules:
                if (sim[k-2] == r.pattern[0] and
                    sim[k-1] == r.pattern[1] and
                    sim[k] == r.pattern[2] and
                    sim[k+1] == r.pattern[3] and
                    sim[k+2] == r.pattern[4]):
                        nextgen[k] = '#'
        sim = nextgen
    return sum(sim.keys())

def aoc12(filename):
    state, rules = load(filename)
    return [p1(state, rules), None]

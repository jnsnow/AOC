from itertools import count
from collections import namedtuple

Point4D = namedtuple('Point', ['x', 'y', 'z', 'w'])

def manhattan(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z) + abs(a.w - b.w)

def adjacent(const1, const2):
    for point in const1:
        for other in const2:
            if manhattan(point, other) <= 3:
                return True

def collapse_constellations(constellations):
    while True:
        n = len(constellations)
        new_constellations = {}
        for i, constellation in constellations.items():
            if not constellation:
                continue
            new_constellations[i] = constellation
            constellations[i] = []
            for j, otherconst in constellations.items():
                if i == j:
                    continue
                if adjacent(constellation, otherconst):
                    new_constellations[i].extend(otherconst)
                    constellations[j] = []
        constellations = new_constellations
        if len(constellations) == n:
            return constellations

def p1(filename):
    points = []
    with open(filename, 'r') as f:
        for line in f:
            points.append(Point4D(*[int(n) for n in line.strip().split(',')]))

    constellations = {}
    counter = count(0)
    for point in points:
        constellations[next(counter)] = [point]

    constellations = collapse_constellations(constellations)
    return len(constellations)

def p2():
    return "boop!"

def aoc25(filename):
    return p1(filename)

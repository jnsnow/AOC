import re
from collections import namedtuple
from itertools import product

Claim = namedtuple('Claim', ['id', 'dx', 'dy', 'x', 'y'])

def read_claim(line):
    res = re.match('#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)', line)
    return Claim(res[1], int(res[2]), int(res[3]), int(res[4]), int(res[5]))

def overlaps(left, right):
    if (left.dx + left.x < right.dx) or (right.dx + right.x < left.dx):
        return False
    if (left.dy + left.y < right.dy) or (right.dy + right.y < left.dy):
        return False
    return True

def p1(claims):
    fabric = {}
    for claim in claims:
        for coord in product(range(claim.dx, claim.dx + claim.x),
                             range(claim.dy, claim.dy + claim.y)):
            fabric[coord] = fabric.get(coord, 0) + 1
    return len([x for x in fabric.values() if x > 1])

def p2(claims):
    for claim in claims:
        disqual = False
        for other in claims:
            if claim.id == other.id:
                continue
            if overlaps(claim, other):
                disqual = True
                break
        if not disqual:
            return int(claim.id)

def aoc03(filename):
    f = open(filename, "r")
    claims = [read_claim(line) for line in f]
    return [p1(claims), p2(claims)]

#!/usr/bin/python3

from Point import Point
from SparseGrid import SparseGrid
from collections import Counter

class ChronalPoint(Point):
    # the "locality" of a point is the sum of the
    # manhattan distance to all other points.
    def locality(self, points):
        return sum([self.manhattan(p) for p in points])

def load(filename):
    # Read in list of points in "x, y\n" format
    points = []
    with open(filename, 'r') as f:
        for line in f:
            xy = (int(n) for n in line.strip().split(','))
            points.append(ChronalPoint(*xy))

    return points

def p1(points):
    grid = SparseGrid(ChronalPoint)
    for p in points:
        grid[p] = p

    for c in grid.coordinates():
        distances = sorted([(p.manhattan(c), p) for p in points])
        if distances[0][0] != distances[1][0]:
            grid[c] = distances[0][1]

    # Collect the nearest neighbors from any points on the edge of
    # the bounding box, under the premise that they are infinite
    edges = set()
    lower, upper = grid.bounds()
    for x in range(lower.x, upper.x + 1):
        edges.add(grid[ChronalPoint(x, lower.y)])
        edges.add(grid[ChronalPoint(x, upper.y)])
    for y in range(lower.y, upper.y + 1):
        edges.add(grid[ChronalPoint(lower.x, y)])
        edges.add(grid[ChronalPoint(upper.x, y)])

    cnt = Counter((c for c in grid.grid.values() if c not in edges))
    common = cnt.most_common(1)[0]
    return common[1]


def p2(points, threshold=10000):
    # Compute a point that's reasonably centered
    xvals = [p.x for p in points]
    yvals = [p.y for p in points]
    xavg = sum(xvals)/len(points)
    yavg = sum(yvals)/len(points)
    center = ChronalPoint(int(xavg), int(yavg))

    # Identify neighbors within the threshold distance
    localities = {}
    queue = [center]
    for coordinate in queue:
        if coordinate in localities:
            continue
        locality = coordinate.locality(points)
        if locality < threshold:
            localities[coordinate] = locality
            queue.extend(coordinate.neighbors())

    return len(localities)


def aoc06(filename):
    points = load(filename)
    return [p1(points), p2(points)]

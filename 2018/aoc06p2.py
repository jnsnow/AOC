#!/usr/bin/python3

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)

    def __repr__(self):
        return "Point(x=%d, y=%d)" % (self.x, self.y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def left(self):
        return Point(self.x - 1, self.y)

    def right(self):
        return Point(self.x + 1, self.y)

    def up(self):
        return Point(self.x, self.y + 1)

    def down(self):
        return Point(self.x, self.y - 1)

    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    @property
    def neighbors(self):
        return [self.left(), self.right(), self.up(), self.down()]

def calc_locality(coordinate, points):
    distances = [coordinate.manhattan(p) for p in points]
    return sum(distances)

def aoc6p2(filename, threshold=10000):
    points = []

    # Read in list of points in "x, y\n" format
    with open(filename, 'r') as f:
        for line in f:
            x, y = line.split(',')
            points.append(Point(int(x), int(y)))

    # Compute a point that's reasonably centered
    xvals = [p.x for p in points]
    yvals = [p.y for p in points]
    xavg = sum(xvals)/len(points)
    yavg = sum(yvals)/len(points)
    center = Point(int(xavg), int(yavg))

    # Identify neighbors within the threshold distance
    localities = {}
    queue = [center]
    for coordinate in queue:
        if coordinate in localities:
            continue
        locality = calc_locality(coordinate, points)
        if locality < threshold:
            localities[coordinate] = locality
            queue.extend(coordinate.neighbors)

    return len(localities)

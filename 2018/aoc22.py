from SparseGrid import SparseGrid
from Point import Point
from collections import namedtuple
import re

equipment = {
    'T': {'T', 'C'},
    '.': {'T', 'C'},
    '=': {'C', 'N'},
    '|': {'T', 'N'}
}

class CaveSystem:
    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        self.indices = SparseGrid(Point)
        self.erosions = SparseGrid(Point)
        self.grid = SparseGrid(Point)

    def region_risk(self):
        calc = 0
        for x in range(0, self.target.x + 1):
            for y in range(0, self.target.y + 1):
                p = Point(x, y)
                calc += self.risk(p)
        return calc

    def generate_map(self, extra=0):
        for x in range(0, self.target.x + extra + 1):
            for y in range(0, self.target.y + extra + 1):
                p = Point(x, y)
                self.grid[p] = self.tile(p)

    def index(self, p):
        if self.indices[p] is not None:
            return indices[p]
        if p == (0, 0) or p == self.target:
            self.indices[p] = 0
        elif p.y == 0:
            self.indices[p] = p.x * 16807
        elif p.x == 0:
            self.indices[p] = p.y * 48271
        else:
            a = Point(p.x - 1, p.y)
            b = Point(p.x, p.y - 1)
            ero_a = self.erosion(a)
            ero_b = self.erosion(b)
            self.indices[p] = ero_a * ero_b
        return self.indices[p]

    def erosion(self, p):
        if self.erosions[p] is not None:
            return self.erosions[p]
        self.erosions[p] = (self.index(p) + self.depth) % 20183
        return self.erosions[p]

    def risk(self, p):
        ero = self.erosion(p)
        return ero % 3

    def tile(self, p):
        risk = self.risk(p)
        if risk == 0:
            return "."
        elif risk == 1:
            return "="
        elif risk == 2:
            return "|"

    def ttype(self, p):
        names = { ".": "rocky",
                  "=": "wet",
                  "|": "narrow" }
        return names[self.tile(p)]

    def summary(self, p):
        print(self.index(p))
        print(self.erosion(p))
        print(self.ttype(p))

    def dijkstra(self, point, destination, equip):
        """Dijkstra's algorithm returning the lowest cost to travel from A to B,
        Qualified by the equipment held upon arrival."""
        travel_times = {}
        travel_times[(point, equip)] = 0
        queue = [(point, equip)]
        while queue:
            point, equip = queue.pop(0)
            time = travel_times[(point, equip)]
            for neighbor in point.neighbors():
                if not self.grid[neighbor]:
                    continue

                if equip in equipment[self.grid[neighbor]]:
                    # We can visit this neighbor directly, and we know it's faster than switching.
                    # It is never correct to switch prematurely, because we will discover if switching
                    # at the target node would have been worthwhile if it concludes it needs to switch
                    # to travel to one of its neighbors -- i.e., because addition is commutative,
                    # there's no reason to do it NOW.
                    newequip = equip
                    ttn = (time + 1)
                else:
                    # we MUST switch to reach neighbor.
                    compat = equipment[self.grid[point]] & equipment[self.grid[neighbor]]
                    assert(len(compat) == 1)
                    newequip = list(compat)[0]
                    ttn = (time + 8)

                # Now that we know the cost and equipment, visit the neighbor.
                if (ttn < travel_times.get((neighbor, newequip), float("inf"))):
                    travel_times[(neighbor, newequip)] = ttn
                    queue.append((neighbor, newequip))

        return {k: travel_times.get((destination, k)) for k in 'TCN'}

    def rescue(self):
        """Rescue that reindeer."""
        times = self.dijkstra(Point(0, 0), self.target, 'T')
        final_times = []

        if times.get('T'):
            final_times.append(times['T'])
        if times.get('C'):
            final_times.append(times['C'] + 7)

        return min(final_times)


def load(filename):
    with open(filename, 'r') as f:
        depth = int(re.match(r"depth: ([\d]+)", f.readline())[1])
        tgroup = re.match(r"target: ([\d]+),([\d]+)", f.readline())
        target = Point(int(tgroup[1]), int(tgroup[2]))
    return CaveSystem(depth, target)

def p1(filename):
    cave = load(filename)
    return cave.region_risk()

def p2(filename):
    cave = load(filename)
    # Generate the map a little beyond the target.
    # No, I can't prove that this is generally sufficient.
    # A better alternative would be generating on-demand with A*.
    cave.generate_map(extra=7)
    return cave.rescue()

def aoc22(filename):
    return (p1(filename), p2(filename))

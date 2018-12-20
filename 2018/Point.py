import itertools
from collections import namedtuple

BasicPoint = namedtuple('BasicPoint', ['x', 'y'])

class Point(BasicPoint):
    def west(self, n=1):
        return type(self)(self.x - n, self.y)

    def east(self, n=1):
        return type(self)(self.x + n, self.y)

    def north(self, n=1):
        return type(self)(self.x, self.y - n)

    def northeast(self, n=1):
        return type(self)(self.x + 1, self.y - n)

    def northwest(self, n=1):
        return type(self)(self.x + 1, self.y - n)

    def south(self, n=1):
        return type(self)(self.x, self.y + n)

    def southeast(self, n=1):
        return type(self)(self.x + 1, self.y + n)

    def southwest(self, n=1):
        return type(self)(self.x - 1, self.y + n)

    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def neighbors(self):
        return [self.north(), self.east(), self.south(), self.west()]

    def ring(self):
        # Return all surrounding 8 points, careful to exclude ourselves.
        return [type(self)(x, y) for x, y in
                itertools.product([self.x - 1, self.x, self.x + 1],
                                  [self.y - 1, self.y, self.y + 1])
                if (x, y) != self]

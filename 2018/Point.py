import itertools
from collections import namedtuple

BasicPoint = namedtuple('BasicPoint', ['x', 'y'])

class Point(BasicPoint):
    # Cardinals
    def north(self, n=1):
        return type(self)(self.x, self.y - n)
    def east(self, n=1):
        return type(self)(self.x + n, self.y)
    def south(self, n=1):
        return type(self)(self.x, self.y + n)
    def west(self, n=1):
        return type(self)(self.x - n, self.y)

    # Ordinals
    def northeast(self, n=1):
        return type(self)(self.x + n, self.y - n)
    def southeast(self, n=1):
        return type(self)(self.x + n, self.y + n)
    def southwest(self, n=1):
        return type(self)(self.x - n, self.y + n)
    def northwest(self, n=1):
        return type(self)(self.x + n, self.y - n)

    # Cardinal Aliases
    def up(self, *args):
        return self.north(*args)
    def right(self, *args):
        return self.east(*args)
    def down(self, *args):
        return self.south(*args)
    def left(self, *args):
        return self.west(*args)

    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def neighbors(self):
        yield self.north()
        yield self.east()
        yield self.south()
        yield self.west()

    def adjacent(self):
        return self.neighbors()

    def ring(self):
        # Return all surrounding 8 points, careful to exclude ourselves.
        return [type(self)(x, y) for x, y in
                itertools.product([self.x - 1, self.x, self.x + 1],
                                  [self.y - 1, self.y, self.y + 1])
                if (x, y) != self]

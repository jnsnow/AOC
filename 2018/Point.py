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

    def ring(self, n=1):
        """Generate all points in the nth ring outward from this point,
        in clockwise order starting at the upper-left corner.
        at n=1, this is the 8 surrounding points.
        at n=2, this is the 16 points that neighbor the previous 8."""
        # Top Row, left-to-right;
        for dx in range(-n, n + 1):
            yield type(self)(self.x + dx, self.y - n)
        # Right Wall, top-to-bottom:
        for dy in range(-n + 1, n):
            yield type(self)(self.x + n, self.y + dy)
        # Bottom Row, right-to-left:
        for dx in reversed(range(-n, n + 1)):
            yield type(self)(self.x + dx, self.y + n)
        # Left Well, bottom-to-top:
        for dy in reversed(range(-n + 1, n)):
            yield type(self)(self.x - n, self.y + dy)

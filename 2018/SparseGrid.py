from collections import defaultdict

class SparseGrid:
    def __init__(self, cls, default=None):
        self.grid = defaultdict(lambda: default)
        self._cls = cls
        self._d = 2
        self._default = default

    def __setitem__(self, key, value):
        self.grid[key] = value

    def __getitem__(self, key):
        return self.grid.get(key, self._default)

    def bounds(self):
        lowers = [float('inf')] * self._d
        uppers = [float('-inf')] * self._d

        for point in self.grid:
            for d in range(self._d):
                if point[d] < lowers[d]:
                    lowers[d] = point[d]
                if point[d] > uppers[d]:
                    uppers[d] = point[d]

        lower = self._cls(*lowers)
        upper = self._cls(*uppers)
        return (lower, upper)

    def print(self):
        # TODO: generalize to [1-3] dimensions
        assert(self._d == 2)
        lower, upper = self.bounds()
        for y in range(lower.y, upper.y + 1):
            for x in range(lower.x, upper.x + 1):
                p = self._cls(x, y)
                print(self[p], end='')
            print('')

    def points(self, function=None):
        """Return only points that have been set"""
        return filter(function,
                      (key for key in self.grid.keys()))

    def coordinates(self):
        """Return all coordinates inside the bounding box"""
        # TODO: generalize to N dimensions
        lower, upper = self.bounds()
        for y in range(lower.y, upper.y + 1):
            for x in range(lower.x, upper.x + 1):
                p = self._cls(x, y)
                yield p

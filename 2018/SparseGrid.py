from collections import defaultdict

class SparseGrid:
    def __init__(self, cls, default=None):
        self.grid = defaultdict(lambda: default)
        self._cls = cls
        self._d = 2

    def __setitem__(self, key, value):
        self.grid[key] = value

    def __getitem__(self, key):
        return self.grid[key]

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
        lower, upper = self.bounds()
        for y in range(lower.y, upper.y + 1):
            for x in range(lower.x, upper.x + 1):
                p = self._cls(x, y)
                print(self[p], end='')
            print('')

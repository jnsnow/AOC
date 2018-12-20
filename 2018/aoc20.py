from Point import Point
from collections import namedtuple
from SparseGrid import SparseGrid

Dir = namedtuple('Dir', ['tile', 'fn'])

def draw_map(grid, sequence, loc):
    cmap = { 'N': Dir('-', type(loc).north),
             'E': Dir('|', type(loc).east),
             'S': Dir('-', type(loc).south),
             'W': Dir('|', type(loc).west) }
    startloc = loc
    while sequence:
        char = sequence.pop(0)
        if char == '^':
            draw_map(grid, sequence, loc)
        elif char in cmap:
            grid[cmap[char].fn(loc)] = cmap[char].tile
            loc = cmap[char].fn(loc, 2)
            grid[loc] = '.'
        elif char == '(':
            draw_map(grid, sequence, loc)
        elif char == '|':
            loc = startloc
        elif char == ')':
            return
        elif char == '$':
            return
        else:
            assert(False)

def find_max(grid, point, threshold=1000):
    visited = set()
    dist = 0
    queue = [(point, dist)]
    maxdist = 0
    threshcount = 0
    while queue:
        point, dist = queue.pop(0)
        if point in visited:
            continue
        visited.add(point)
        maxdist = max(dist, maxdist)
        if dist >= threshold:
            threshcount += 1
        # North
        if grid[point.north()] == '-':
            queue.append((point.north(2), dist + 1))
        # East
        if grid[point.east()] == '|':
            queue.append((point.east(2), dist + 1))
        # South
        if grid[point.south()] == '-':
            queue.append((point.south(2), dist + 1))
        # West
        if grid[point.west()] == '|':
            queue.append((point.west(2), dist + 1))
    return maxdist, threshcount


def aoc20(filename):
    with open(filename, "r") as f:
        line = f.readline().strip()
        sequence = list(line)

    origin = Point(0, 0)
    grid = SparseGrid(Point, '#')
    grid[origin] = 'X'

    draw_map(grid, sequence, origin)
    return find_max(grid, origin)

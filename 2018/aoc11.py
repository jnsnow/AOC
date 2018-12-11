import logging

def powlevel(input, x, y):
    rack = x + 10
    pow = rack * y
    pow += input
    pow = pow * rack
    pow = int(pow / 100) % 10
    pow = pow - 5
    return pow

def cubelevel(grid, x, y, size=3):
    sum = 0
    for locx in range(x, x + size):
        for locy in range(y, y + size):
            sum += grid[(locx, locy)]
    return sum

def hypercube(grid, x, y):
    """from a starting coordinate x,y compute the largest square"""
    total = 0
    squares = {}
    # Easiest to calculate with a box of size 1 as s=0
    for s in range(0, 301):
        if (x + s > 300) or (y + s > 300):
            break
        # lower-right hand corner of the box
        total += grid[(x+s, y+s)]
        # right-wall of the box
        total += sum([grid[((x+s), vy)] for vy in range(y, y+s)])
        # bottom-wall of the box
        total += sum([grid[(vx, (y+s))] for vx in range(x, x+s)])
        squares[s+1] = total
    return max(squares.items(), key=lambda foo: foo[1])

def p1(grid):
    cubes = {}
    for x in range(1, 301 - 3):
        for y in range(1, 301 - 3):
            cubes[(x,y)] = cubelevel(grid, x, y)
    (x, y), val = max(cubes.items(), key=lambda f: f[1])
    return "%d,%d" % (x, y)

def p2(grid):
    # Takes a hot minute, but gets faster with each 'x' ...
    supersums = {}
    for x in range(1, 301):
        logging.debug("x=%d", x)
        for y in range(1, 301):
            answ = hypercube(grid, x, y)
            supersums[(x,y,answ[0])] = answ[1]
    (x, y, s), val = max(supersums.items(), key=lambda f: f[1])
    return "%d,%d,%s" % (x, y, s)

def aoc11(input):
    grid = {}
    for x in range(1, 301):
        for y in range(1, 301):
            grid[(x,y)] = powlevel(input, x, y)
    return [p1(grid), p2(grid)]

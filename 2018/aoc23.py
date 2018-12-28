# This is... PROBABLY not a generalized solution.
# But this is how I came to my answer using a series of heuristics,
# that got me close enough to a point where I could just bruteforce the answer.

import re
from collections import namedtuple

Point3D = namedtuple('Point3D', ['x', 'y', 'z'])

def neighbors3D(p, adj=1):
    """Yield all six one-step neighbors from point p."""
    yield Point3D(p.x, p.y, p.z - adj)
    yield Point3D(p.x, p.y, p.z + adj)
    yield Point3D(p.x, p.y - adj, p.z)
    yield Point3D(p.x, p.y + adj, p.z)
    yield Point3D(p.x - adj, p.y, p.z)
    yield Point3D(p.x + adj, p.y, p.z)

class Nanobot:
    def __init__(self, r, x, y, z):
        self.pos = Point3D(x, y, z)
        self.r = r
    def __eq__(self, other):
        return self.pos == other.pos and self.r == other.r
    def __hash__(self):
        return hash((self.pos, self.r))

def manhattan(p, o):
    """Compute the manhattan distance between two 3D points."""
    dx = abs(p.x - o.x)
    dy = abs(p.y - o.y)
    dz = abs(p.z - o.z)
    return dx + dy + dz

def scan_nanobots(filename):
    """From a file, return a list of Nanobot objects."""
    nanobots = []
    with open(filename, 'r') as f:
        for line in f:
            m = re.search(r"pos=<(.+?)>, r=(\d+)\n", line)
            pos = m[1].split(',')
            r = int(m[2])
            nanobot = Nanobot(r, *[int(w) for w in pos])
            nanobots.append(nanobot)
    return nanobots

def in_range_of(nanobots, bot):
    """For a given set of nanobots and a specific nanobot,
    count how many (self-inclusive) are within its range."""
    distances = []
    for other in nanobots:
        dist = manhattan(bot.pos, other.pos)
        if dist <= bot.r:
            distances.append(dist)
    return len(distances)

def in_range_from(nanobots, point):
    """For a given set of nanobots and an arbitrary point,
    count how many bots it is within range of."""
    distances = []
    for other in nanobots:
        dist = manhattan(point, other.pos)
        if dist <= other.r:
            distances.append(dist)
    return len(distances)

def cull_nanobots(nanobots, threshold):
    """Return a list of nanobots that satisfy a novel criterion; that this
    nanobot intersects with at least as many as int(threshold) other nanobots.
    The big idea here is that if we know that a certain point is in range of
    e.g. 822 points that no nanobot that intersects with less than 821 other
    nanobots will be part of the eventual solution set, so it can be culled.
    Then, iteratively, better heuristics can be applied on the remaining set,
    increasing the threshold until the best known point and the size of the
    remaining set are identical -- giving us our solution."""
    result = []
    for nanobot in nanobots:
        score = 0
        for other in nanobots:
            dist = manhattan(nanobot.pos, other.pos)
            if dist <= (nanobot.r + other.r):
                score += 1
        if score >= threshold:
            result.append(nanobot)
    return result

def minimize_magnitudes(nanobots, cbkp):
    """Visualizing a nanobot's range as a voxelated sphere, we can compute an
    integer that represents how far we need to travel to be within that sphere
    or how far inside the sphere we are.
    This value is referred to as the rdiff below.
    When this value is negative, we are outside of the sphere and when it is
    positive we are inside the sphere. This phase-one heuristic seeks to minimize
    the total distances in general: be as close to the radii boundaries as
    possible in either the inside or outside direction to find a more centrally
    located point.
    This heuristic tries to close the gap by moving distances that are 1% the
    average distance to all sphere hulls, then dropping to 0.5%, 0.25%, and so
    on whenever we can't get closer.
    In practice, this finds a local minima extremely quickly."""
    rdiffs = [nanobot.r - manhattan(nanobot.pos, cbkp) for nanobot in nanobots]
    magnitudes = [abs(rdiff) for rdiff in rdiffs]
    bestscore = sum(magnitudes)
    bestneighbor = cbkp
    keep_searching = True
    reduction = 1
    while keep_searching:
        keep_searching = False
        # Try to close the gap at about 1%; or once that becomes
        # too wide of a window, 0.5%, 0.25%, etc.
        average = sum(magnitudes) / len(magnitudes)
        increment = int(average / (100 * reduction))
        increment = max(1, increment)
        for neighbor in neighbors3D(bestneighbor, increment):
            rdiffs = [nanobot.r - manhattan(nanobot.pos, neighbor) for nanobot in nanobots]
            magnitudes = [abs(rdiff) for rdiff in rdiffs]
            score = sum(magnitudes)
            if score <= bestscore:
                keep_searching = True
                bestscore = score
                bestneighbor = neighbor
        if not keep_searching and increment > 1:
            print("Window is too wide, dropping down")
            reduction = reduction * 2
            keep_searching = True
        print("bestscore %d loc %s incr %d" % (bestscore, str(bestneighbor),
                                               increment))
    return bestneighbor

def minimize_negative_rdists(nanobots, cbkp):
    """minimize magnitudes will eventually get stuck on a local minima that's
    likely close to the real answer. This version minimizes only the negative
    r-differences which may either find the actual correct answer or another
    local minima."""
    rdiffs = [nanobot.r - manhattan(nanobot.pos, cbkp) for nanobot in nanobots]
    negatives = [abs(rdiff) for rdiff in rdiffs if rdiff < 0]
    bestscore = sum(negatives)
    bestneighbor = cbkp
    keep_searching = True
    while keep_searching:
        keep_searching = False
        for neighbor in neighbors3D(bestneighbor):
            rdiffs = [nanobot.r - manhattan(nanobot.pos, neighbor) for nanobot in nanobots]
            negatives = [abs(rdiff) for rdiff in rdiffs if rdiff < 0]
            score = sum(negatives)
            if score <= bestscore:
                keep_searching = True
                bestscore = score
                bestneighbor = neighbor
        print("bestscore %d loc %s" % (bestscore, str(bestneighbor)))
    return bestneighbor

def guess_maximal_intersection(nanobots, point):
    """Iterate using two different heuristics to zero in on either the answer,
    or a point very likely to be close to the answer."""
    # Cull the list to exclude poorly connected bots
    best_score = in_range_from(nanobots, point)
    picobots = cull_nanobots(nanobots, best_score)
    print("culled %d bots down to %d" % (len(nanobots), len(picobots)))
    last_point = None
    loops = 0

    while True:
        loops += 1
        # Minimize our distance to the edges of all remaining signal
        # boundaries, moving closer to the edges of reception if we
        # are outside OR inside signal range.
        print("minimizing distance to all remaining signal radii")
        point = minimize_magnitudes(picobots, point)
        score = in_range_from(nanobots, point)
        print("point %s is in range of %d bots" % (str(point), score))
        if score == len(picobots):
            print("Found a maximally intersected point! iterations=%d" % loops)
            return point, picobots
        elif score > best_score:
            best_score = score
            tmp = len(picobots)
            picobots = cull_nanobots(picobots, best_score)
            print("culled %d bots down to %d" % (tmp, len(picobots)))
            if len(picobots) < tmp:
                # OK, we have better intel now.
                continue

        # Minimize our distance to any edges of any signal spheres
        # we are outside of, without caring about our distance to
        # the edges of any signal spheres we're inside of.
        print("closing gap to remaining exterior signal radii")
        point = minimize_negative_rdists(picobots, point)
        if point == last_point:
            print("Heuristic is not improving, returning best known point. iterations=%d" % loops)
            return point, picobots
        last_point = point
        score = in_range_from(nanobots, point)
        print("point %s is in range of %d bots" % (str(point), score))
        if score == len(picobots):
            print("Found a maximally intersected point! iterations=%d" % loops)
            return point, picobots
        if score > best_score:
            best_score = score
            tmp = len(picobots)
            picobots = cull_nanobots(picobots, best_score)
            print("culled %d bots down to %d" % (tmp, len(picobots)))
            if len(picobots) < tmp:
                # OK, we have better intel now.
                continue


def p1(filename):
    nanobots = scan_nanobots(filename)
    strongest = max(nanobots, key=lambda nanobot: nanobot.r)
    return in_range_of(nanobots, strongest)

def p2(filename):
    origin = Point3D(0, 0, 0)
    nanobots = scan_nanobots(filename)
    print("read in %d nanobots" % len(nanobots))

    # Find the best-located bot
    exocounts = {}
    for bot in nanobots:
        exocounts[bot] = in_range_from(nanobots, bot.pos)
    best_nano, best_score = max(exocounts.items(), key=lambda kv: kv[1])
    print("Found the nanobot in range of the most other nanobots;"
          "pos: %s; in range of: %d" % (str(best_nano.pos), best_score))

    # Make our best guess at the maximally intersected point
    best, picobots = guess_maximal_intersection(nanobots, best_nano.pos)

    # We either have an exact answer or we're likely pretty close.
    # Construct a cube based on the cumulative distances to the remaining
    # signal spheres we're outside of and search within that cube.
    rdiffs = [nanobot.r - manhattan(nanobot.pos, best) for nanobot in picobots]
    diff = sum([abs(rdiff) for rdiff in rdiffs if rdiff < 0])
    candidates = set()
    for x in range(best.x - diff, best.x + diff + 1):
        for y in range(best.y - diff, best.y + diff + 1):
            for z in range(best.z - diff, best.z + diff + 1):
                p = Point3D(x, y, z)
                score = in_range_from(nanobots, p)
                if score > best_score:
                    candidates = set()
                if score >= best_score:
                    best_score = score
                    candidates.add(p)
                    print("found new best point %s in range of %d" % (str(p), score))

    # OK, which of these is closest to origin?
    final = min(candidates, key=lambda p: manhattan(origin, p))
    return manhattan(origin, final)

def aoc23(filename):
    return (p1(filename), p2(filename))

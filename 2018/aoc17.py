import re
import logging

# Note, instead of using | for corner tiles where it flows down, I use '+' to denote a new "source".

class Source:
    def __init__(self, xy, parent):
        self.x = xy[0]
        self.y = xy[1]
        self.parent = parent
    def pair(self):
        return self.x, self.y
    def __hash__(self):
        return hash(self.x, self.y)
    def __eq__(self, other):
        return (self.x == other.x and
                self.y == other.y)

class Sim:
    def __init__(self, filename):
        self.clay = {}
        self.load(filename)
        self.clay[(500, 0)] = '+'
        self.sources = [Source((500, 0), None)]
        self.compute_bounds()

    def load(self, filename):
        f = open(filename, 'r')
        for line in f:
            m = re.search("x=([0-9]+), y=([0-9]+)\.\.([0-9]+)$", line)
            if m:
                x = int(m[1])
                for y in range(int(m[2]), int(m[3]) + 1):
                    self.clay[(x,y)] = '#'
                continue

            m = re.search("y=([0-9]+), x=([0-9]+)\.\.([0-9]+)$", line)
            y = int(m[1])
            for x in range(int(m[2]), int(m[3]) + 1):
                self.clay[(x,y)] = '#'
        f.close()

    def compute_bounds(self):
        yvals = [key[1] for key in self.clay.keys()]
        self.miny = min(yvals)
        self.maxy = max(yvals)

    def print(self):
        xvals = [key[0] for key in self.clay.keys()]
        for y in range(self.miny, self.maxy + 1):
            for x in range(min(xvals), max(xvals) + 1):
                tile = self.clay.get((x, y), '.')
                print(tile, end='')
            print('')

    def fill_row(self, source, x, y):
        logging.debug("looking at row %d centered on %d" % (y, x))

        # If water overtook the source, go back to the parent source
        if y <= source.y:
            logging.debug("water overflowed our source")
            if source.parent not in self.sources:
                logging.debug("adding parent back to sources queue")
                self.sources.append(source.parent)
            else:
                logging.debug("skipping, parent already in sources queue")
            return False

        left, left_wall = self.find_supported('left', x, y)
        right, right_wall = self.find_supported('right', x, y)

        if left_wall and right_wall:
            logging.debug("filling with solids")
            for x in range(left, right):
                self.clay[(x, y)] = '~'
            return True
        else:
            logging.debug("filling with empties")
            for x in range(left, right):
                self.clay[(x, y)] = '|'
            if not left_wall:
                logging.debug("LHS new source")
                newsource = (left - 1, y)
                assert(self.clay.get(newsource, '.') in '.+')
                self.clay[newsource] = '+'
                self.sources.append(Source(newsource, source))
            if not right_wall:
                logging.debug("RHS new source")
                newsource = (right, y)
                assert(self.clay.get(newsource, '.') in '.+')
                self.clay[newsource] = '+'
                self.sources.append(Source(newsource, source))
            return False

    def run(self):
        while self.sources:
            source = self.sources.pop(0)
            x, y = source.pair()
            logging.debug("source @ (%d,%d) %d left" % (x, y, len(self.sources)))
            fy = self.find_floor(x, y)
            dy = min(fy, self.maxy + 1)
            for y in range(y + 1, dy):
                self.clay[(x, y)] = '|'
            if fy > self.maxy:
                continue
            while self.fill_row(source, x, y):
                y = self.find_floor(source.x, source.y) - 1

    def find_floor(self, x, y):
        while True:
            y += 1
            if y > self.maxy:
                return y
            tile = self.clay.get((x, y), '.')
            if tile in '~#':
                return y

    # returns x, solid=[True|False]
    def find_supported(self, dir, x, y):
        while True:
            if dir == 'left':
                x -= 1
            elif dir == 'right':
                x += 1
            tile = self.clay.get((x, y), '.')
            below = self.clay.get((x, y+1), '.')
            if tile not in '.|+':
                # Water can flow through .|+ tiles
                if dir == 'left':
                    x += 1
                return x, True
            elif below not in '~#':
                # Water must be supported by ~# tiles
                if dir == 'left':
                    x += 1
                return x, False

    def p1_value(self):
        tmp = [v for k,v in self.clay.items() if k[1] > self.miny and k[1] < self.maxy]
        return len([v for v in tmp if v in '~|+'])

    def p2_value(self):
        tmp = [v for k,v in self.clay.items() if k[1] > self.miny and k[1] < self.maxy]
        return len([v for v in tmp if v in '~'])

def aoc17(filename):
    sim = Sim(filename)
    sim.run()
    return [sim.p1_value(), sim.p2_value()]

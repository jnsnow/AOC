import logging
import re
import itertools
import os

class coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def adjacent(self):
        return [coordinate(self.x, self.y + 1),
                coordinate(self.x, self.y - 1),
                coordinate(self.x + 1, self.y),
                coordinate(self.x - 1, self.y)]

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return "coordinate(x=%d, y=%d)" % (self.x, self.y)

    def __str__(self):
        return "(%d,%d)" % (self.x, self.y)


class NPC:
    def __init__(self, board, id, type, x, y):
        self.board = board
        self.id = id
        self.type = type
        self.pos = coordinate(x, y)
        self.power = 3
        self.hp = 200
        self.alive = True
        self.candidates = []
        self.panic = False

    def __repr__(self):
        return "NPC(%d,%s,%d,%d,%d)" % (self.id, self.type, self.pos.x, self.pos.y, self.hp)

    def __str__(self):
        return repr(self)

    def find_candidates(self):
        self.candidates = self.board.enemies_near(self)

    def _movement_candidates(self):
        targets = self.board.enemies(self.type)
        assert(targets)
        destinations = []
        for target in targets:
            for coord in target.adjacent():
                if self.board.tile(coord) == '.':
                    destinations.append(coord)

        if not destinations:
            logging.info("%s:%d has no available destinations", self.type, self.id)
            return None

        logging.debug("found %d candidate destinations", len(destinations))
        return destinations

    def _nearest_destination(self, destinations):
        distances = []
        valid_distances = []
        maximum = float("inf")
        for dest in destinations:
            distance = self.board.distance(self.pos, dest, maximum)
            distances.append(distance)
            if distance is not None:
                valid_distances.append(distance)
                maximum = min(distance, maximum)
        if not valid_distances:
            logging.info("%s:%d can't reach any of their destinations", self.type, self.id)
            return None, None
        minima = min(valid_distances)
        candidates = []
        for dest, dist in zip(destinations, distances):
            if dist == minima:
                candidates.append(dest)
                logging.debug("candidate destination %s dist %d", str(dest), dist)

        assert(candidates)
        return sorted(candidates, key=lambda p: (p.y, p.x))[0], minima

    def _determine_step(self, destination, distance):
        compass = {}
        for step in self.pos.adjacent():
            if self.board.tile(step) != '.':
                logging.debug("tile is unwalkable %s", self.board.tile(step))
                continue
            step_distance = self.board.distance(step, destination)
            if step_distance is None:
                continue
            distance = min(distance, step_distance)
            compass[step] = step_distance

        candidates = [s for s, d in compass.items() if d == distance]
        candidates = sorted(candidates, key=lambda p: (p.y, p.x))
        return candidates[0]

    def move(self):
        logging.debug("%s:%d attempting to move...", self.type, self.id)
        destinations = self._movement_candidates()
        if not destinations:
            return

        destination, distance = self._nearest_destination(destinations)
        if not destination:
            return
        logging.debug("%s:%d wants to move towards %s", self.type, self.id, str(destination))

        step = self._determine_step(destination, distance)
        self.board.move(self, step)
        return True

    def attack(self):
        if self.candidates:
            target = min(self.candidates, key=lambda n: (n.hp, n.pos.y, n.pos.x))
            logging.info("%s:%d attacks %s:%d!", self.type, self.id, target.type, target.id)
            target.damage(self.power)

    def turn(self):
        if not self.alive:
            return
        if sum(self.board.factions.values()) == self.board.factions[self.type]:
            raise StopIteration("Simulation is over")
        self.find_candidates()
        if not self.candidates:
            if not self.move():
                return
            self.find_candidates()
        self.attack()

    def damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            #owowowow
            self.die()

    def die(self):
        logging.info("%s:%d has died!", self.type, self.id)
        self.alive = False
        self.board.remove(self)
        if self.panic:
            raise ArithmeticError("%s:%d has died!" % (self.type, self.id))

    def adjacent(self):
        return self.pos.adjacent()

    def in_range(self, other):
        return self.pos in other.adjacent()

class Board:
    def __init__(self, filename, elfpanic=False, elfpower=3):
        self.rounds = 0
        self.state = []
        self.npcs = []
        self.objects = {}
        self.factions = {}
        f = open(filename, "r")
        line_counter = itertools.count()
        npc_counter = itertools.count()
        for line in f:
            lineNo = next(line_counter)
            for m in re.finditer('[GE]', line):
                npc = NPC(self, next(npc_counter), m.group(), m.start(), lineNo)
                if elfpanic and npc.type == 'E':
                    npc.power = elfpower
                    npc.panic = True
                self.npcs.append(npc)
                self.objects[npc.pos] = npc
                self.factions[npc.type] = self.factions.get(npc.type, 0) + 1
            self.state.append(list(line.strip()))

    def round(self):
        self.npcs = [npc for npc in self.npcs if npc.alive]
        self.npcs = sorted(self.npcs, key=lambda n: (n.pos.y, n.pos.x))
        for npc in self.npcs:
            npc.turn()
        self.rounds += 1

    def print_map(self):
        for row in self.state:
            print(''.join(row))

    def enemies(self, asking_type):
        return [npc for npc in self.npcs if npc.type != asking_type and npc.alive]

    def run(self, visual=False):
        while True:
            if visual:
                os.system('clear')
                self.print_map()
            try:
                self.round()
            except StopIteration:
                if visual:
                    os.system('clear')
                    self.print_map()
                hp = sum([n.hp for n in self.npcs if n.alive])
                return self.rounds * hp

    def tile(self, coord):
        return self.state[coord.y][coord.x]

    def set_tile(self, coord, char):
        self.state[coord.y][coord.x] = char

    def distance(self, start, end, maximum=None):
        visited = set()
        queue = []
        queue.append((start, 0))
        while queue:
            queue = sorted(queue, key=lambda q: q[1])
            here, distance = queue.pop(0)
            if here in visited:
                # oops, something visited us in the meantime?
                continue
            logging.debug("visiting (%d,%d) @ distance %d", here.x, here.y, distance)
            if here == end:
                logging.debug("found %s --> %s, distance %d", str(start), str(end), distance)
                return distance
            visited.add(here)
            # OK, investigating children/neighbors:
            distance += 1
            if maximum and distance > maximum:
                continue
            for near in here.adjacent():
                if near in visited:
                    continue
                elif self.tile(near) == '.':
                    logging.debug("queueing (%d,%d)", near.x, near.y)
                    queue.append((near, distance))
        return None

    def move(self, whom, to):
        assert(self.tile(to) == '.')
        del self.objects[whom.pos]
        self.set_tile(whom.pos, '.')
        whom.pos = to
        self.objects[whom.pos] = whom
        self.set_tile(whom.pos, whom.type)

    def remove(self, whom):
        del self.objects[whom.pos]
        self.set_tile(whom.pos, '.')
        self.factions[whom.type] -= 1

    def enemies_near(self, whom):
        enemies = []
        for pos in whom.adjacent():
            if pos in self.objects:
                other = self.objects[pos]
                if other.type != whom.type and other.alive:
                    enemies.append(self.objects[pos])
        return enemies


def p1(filename):
    board = Board(filename)
    return board.run()

def p2(filename, visual=False):
    results = {}
    epr = [3, 200]
    # Use a binary search between 3,200
    while True:
        ep = int((epr[1] - epr[0])/2 + epr[0])
        board = Board(filename, elfpanic=True, elfpower=ep)
        try:
            results[ep] = board.run(visual=visual)
            epr[1] = ep
        except ArithmeticError:
            epr[0] = ep
        if epr[1] - epr[0] == 1:
            return results[epr[1]]

def aoc15(filename):
    return [p1(filename), p2(filename)]

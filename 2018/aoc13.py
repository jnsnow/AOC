import re
import itertools
import logging

cartchars = '^>v<'

class Cart:
    def __init__(self, char, line, pos, id, sim):
        self.char = char
        self.line = line
        self.pos = pos
        self.id = id
        self.sim = sim
        self.turn = 0
        self.ctype = cartchars.find(self.char)
        if (self.char == '>' or
            self.char == '<'):
            self.track = '-'
        if (self.char == 'v' or
            self.char == '^'):
            self.track = '|'
        self.crashed = False

    def __str__(self):
        return "cart %d facing %s at (%d,%d) over track %s" % (self.id, self.char, self.pos, self.line, self.track)

    def coord(self):
        return "%d,%d" % (self.pos, self.line)

    def crash(self):
        self.crashed = True
        self.char = 'X'
        logging.info("CRASH %s", str(self))
        self.sim[self.line][self.pos] = self.track

    def move(self):
        if self.char == '>':
            self.pos += 1
        elif self.char == '<':
            self.pos -= 1
        elif self.char == 'v':
            self.line += 1
        elif self.char == '^':
            self.line -= 1
        else:
            print("chartype went off the rails? %s" % self.char)
            assert(False)

    def tick(self):
        if self.crashed:
            return False

        self.sim[self.line][self.pos] = self.track
        self.move()
        self.track = self.sim[self.line][self.pos]

        if self.track in cartchars:
            self.crash()
            return True
        elif self.track == '\\' and self.char == '^':
            self.char = '<'
        elif self.track == '\\' and self.char == '>':
            self.char = 'v'
        elif self.track == '\\' and self.char == '<':
            self.char = '^'
        elif self.track == '\\' and self.char == 'v':
            self.char = '>'
        elif self.track == '/' and self.char == '>':
            self.char = '^'
        elif self.track == '/' and self.char == 'v':
            self.char = '<'
        elif self.track == '/' and self.char == '^':
            self.char = '>'
        elif self.track == '/' and self.char == '<':
            self.char = 'v'
        elif self.track == '+':
            self.ctype = cartchars.find(self.char)
            if self.turn == 0:
                self.ctype -= 1
            if self.turn == 2:
                self.ctype += 1
            self.char = cartchars[self.ctype % len(cartchars)]
            self.turn = (self.turn + 1) % 3
        elif self.track == '-' or self.track == '|':
            pass
        else:
            print("track under our feet is unknown? %s" % self.track)
            assert(False)

        self.sim[self.line][self.pos] = self.char
        return False

def aoc13(filename):
    f = open(filename, "r")
    lines = f.readlines()

    # Construct Simulation
    sim = []
    for line in lines:
        aline = list(line)
        sim.append(aline)

    # Identify Carts
    carts = []
    cart_id = itertools.count(0)
    for i in range(len(lines)):
        for m in re.finditer('[v<>^]', lines[i]):
            cart = Cart(m.group(), i, m.start(), next(cart_id), sim)
            carts.append(cart)
            logging.info(str(cart))

    # Run Simulation
    answ_p1 = None
    for t in itertools.count():
        carts = sorted([cart for cart in carts if cart.crashed == False],
                       key=lambda c: (c.line, c.pos))
        if len(carts) <= 1:
            answ_p2 = carts[0].coord()
            break
        for cart in carts:
            if cart.tick():
                answ_p1 = answ_p1 or cart.coord()
                for other in carts:
                    if (cart.pos == other.pos and
                        cart.line == other.line and
                        cart.id != other.id):
                        other.crash()

    return [answ_p1, answ_p2]

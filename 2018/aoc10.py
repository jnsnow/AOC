#!/usr/bin/python3

import re
import itertools

class xypair:
    def __init__(self, arg):
        res = re.search("<( *-?[0-9]+),( *-?[0-9]+)", arg)
        self.x = int(res[1])
        self.y = int(res[2])

class Particle:
    def __init__(self, pos, vel):
        self.pos = xypair(pos)
        self.vel = xypair(vel)

def generate_banner(particles, miny, maxy):
    banner = ""
    bitmap = {}
    for p in particles:
        bitmap[(p.pos.x, p.pos.y)] = '#'
    maxx = max(p.pos.x for p in particles)
    minx = min(p.pos.x for p in particles)
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            banner += bitmap.get((x, y), '.')
        banner += "\n"
    return banner

def aoc10(filename):
    banner = ""
    printtime = 0
    particles = []
    converged = False

    # load the data
    f = open(filename, "r")
    for line in f:
        res = re.search("position=(<.*?>) velocity=(<.*?>)", line)
        particles.append(Particle(res[1], res[2]))

    # run the simulation ...
    for t in itertools.count(1):
        # Move the particles along
        maxy = float("-inf")
        miny = float("inf")
        for p in particles:
            p.pos.x += p.vel.x
            p.pos.y += p.vel.y
            maxy = max(p.pos.y, maxy)
            miny = min(p.pos.y, miny)

        # If the y height is less than 10, we can probably see something that looks like a message...
        if abs(maxy - miny) < 10:
            converged = True
        elif converged:
            # pattern is diverging, halt simulation
            return [banner, printtime]
        else:
            continue

        # Get a message, it seems close enough;
        printtime = t
        banner = generate_banner(particles, miny, maxy)
        print(banner)

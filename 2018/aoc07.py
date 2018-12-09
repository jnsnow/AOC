import re
from dataclasses import dataclass
import logging
import itertools

class order:
    def __init__(self, label, requisite):
        self.label = label
        self.requisites = {requisite}
    def addreq(self, requisite):
        self.requisites.add(requisite)

@dataclass
class Instructions:
    ordermap: dict
    requisites: set
    dependents: set

def parse_line(line):
    res = re.search("Step ([A-Z]) must be finished before step ([A-Z]) can begin", line)
    return (res[1], res[2])

def load(filename):
    ordermap = {}
    requisites = set()
    dependents = set()
    f = open(filename, "r")
    for line in f:
        req, dep = parse_line(line)
        requisites.add(req)
        dependents.add(dep)
        if dep not in ordermap:
            ordermap[dep] = order(dep, req)
        else:
            ordermap[dep].addreq(req)
    return Instructions(ordermap, requisites, dependents)

def timecost(letter):
    return 60 + ord(letter) - 64

def p1(instr):
    candidates = list(instr.requisites - instr.dependents)
    sequence = []
    while candidates:
        candidates = sorted(candidates)
        sequence.append(candidates.pop(0))
        for k, v in instr.ordermap.items():
            if (not v.requisites - set(sequence)) and (k not in set(sequence + candidates)):
                candidates.append(k)
    return ''.join(sequence)

def p2(instr, workers=5):
    timers = [0] * workers
    queue = [''] * workers
    sequence = []
    candidates = list(instr.requisites - instr.dependents)
    for t in itertools.count():
        for i in range(workers):
            if timers[i] == 1:
                logging.info("timer %d expiring, adding %c to sequence", i, queue[i])
                sequence.append(queue[i])
                queue[i] = ''
                for k, v in instr.ordermap.items():
                    if not (v.requisites - set(sequence)):
                        if k not in set(sequence + candidates + queue):
                            candidates.append(k)

            if timers[i]:
                timers[i] -= 1

            if timers[i] == 0:
                if candidates:
                    candidates = sorted(candidates)
                    queue[i] = candidates.pop(0)
                    timers[i] = timecost(queue[i])
                    logging.info("adding %c to worker %d", queue[i], i)

        logging.info("%03d - %s", t, ''.join(["[{:s}]".format(queue[i]) for i in range(workers)]))
        if not candidates and set(queue) == {''}:
            break
    return t - 1


def aoc07(filename):
    instr = load(filename)
    return [p1(instr), p2(instr)]

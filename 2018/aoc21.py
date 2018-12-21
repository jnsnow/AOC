from asm import Registers
from asm import Operations
from collections import namedtuple
import logging

Instruction = namedtuple('Instruction', ['op', 'a', 'b', 'c'])

def load(filename):
    program = []
    with open(filename, 'r') as f:
        line = f.readline().strip()
        ipreg = int(line.split('#ip ')[1])
        logging.debug("#ip %d", ipreg)
        for line in f:
            line = line.strip().split(' ')
            instr = Instruction(line[0], *[int(n) for n in line[1:]])
            program.append(instr)
    return ipreg, program

def run(r, ipreg, program):
    ip = 0
    while True:
        r[ipreg] = ip
        #logging.debug("ip=%d %s ", insp, str(r.state))
        instr = program[ip]
        #logging.debug("%s ", program[insp])
        Operations._table[instr.op](r, instr[1:])
        #logging.debug("%s", str(r.state))
        ip = r[ipreg]
        ip += 1
        if ip < 0 or ip >= len(program):
            return

def decompiled(initial):
    # This function is based on my puzzle input, which I assume to be
    # parameterized on the initial value for F in the outer loop.
    fvals = set()
    firstf = 0
    lastf = 0
    f = 0
    while True:
        c = f | 0x10000
        f = initial
        while True:
            f += (c & 255)
            f = f & 0xffffff
            f = f * 65899
            f = f & 0xffffff
            if (c < 256):
                break
            c = int(c / 256)
        if f in fvals:
            logging.info("F value has been seen before: %06x", f)
            return firstf, lastf
        else:
            logging.debug("new F value %06x", f)
            if not fvals:
                firstf = f
            lastf = f
            fvals.add(f)

def aoc21(filename):
    ipreg, program = load(filename)
    r = Registers(n=6)
    # This really cheats and assumes we all have the same fundamental program ...
    assert(program[7].op == 'seti')
    # And assumes this the parameter of that program ...
    constant = program[7][1]
    # Good luck!
    return decompiled(constant)

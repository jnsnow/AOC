from asm import Registers, Operations
from collections import namedtuple
import logging

# Instructions here use a symbolic op instead of numeric opcode
Instruction = namedtuple('Instruction', ['op', 'a', 'b', 'c'])

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
            return r[0]

def p1(program, ipreg):
    r = Registers(n=6)
    result = run(r, ipreg, program)
    return result

def p2(program, ipreg):
    r = Registers(n=6)
    r[0] = 1
    result = run(r, ipreg, program)
    return result

def aoc19(filename):
    program = []
    with open(filename, 'r') as f:
        line = f.readline().strip()
        ipreg = int(line.split('#ip ')[1])
        logging.debug("#ip %d", ipreg)
        for line in f:
            line = line.strip().split(' ')
            instr = Instruction(line[0], *[int(n) for n in line[1:]])
            program.append(instr)

    return [p1(program, ipreg), None]

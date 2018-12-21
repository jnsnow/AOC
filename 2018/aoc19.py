from asm import Registers, asm
from collections import namedtuple
import logging

# Instructions here use a symbolic op instead of numeric opcode
Instruction = namedtuple('Instruction', ['op', 'a', 'b', 'c'])

def run(r, ipreg, program):
    r.ip = 0
    while True:
        r[ipreg] = r.ip
        instr = program[r.ip]
        asm[instr.op].execute(r, *instr[1:])
        r.ip = r[ipreg]
        r.ip += 1
        if r.ip < 0 or r.ip >= len(program):
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

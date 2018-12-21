from asm import Registers, asm, Instruction, Computer
import logging

def p1(program, ipreg):
    sim = Computer(ipreg, program, n=6)
    return sim.run()

def p2(program, ipreg):
    sim = Computer(ipreg, program, n=6)
    sim.r[0] = 1
    return sim.run()

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

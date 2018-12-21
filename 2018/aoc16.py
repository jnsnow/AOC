from asm import *
from collections import namedtuple
import re
import logging

TestCase = namedtuple('TestCase', ['before', 'instruction', 'after'])
Instruction = namedtuple('Instruction', ['opcode', 'a', 'b', 'c'])

def load(filename):
    f = open(filename, 'r')
    lines = f.readlines()

    # Grab TestCases
    i = 0
    tests = []
    while i < len(lines):
        m = re.search("Before: \[([0-9]+), ([0-9]+), ([0-9]+), ([0-9]+)\]", lines[i])
        if not m:
            break
        before = Registers([int(m[j]) for j in range(1,5)])
        m = re.search("([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)", lines[i + 1])
        instruction = Instruction(*[int(m[j]) for j in range(1,5)])
        m = re.search("After:  \[([0-9]+), ([0-9]+), ([0-9]+), ([0-9]+)", lines[i + 2])
        after = Registers([int(m[j]) for j in range(1,5)])
        test = TestCase(before, instruction, after)
        tests.append(test)
        i += 4

    while not lines[i].strip():
        i += 1

    # Grab Simulation
    program = []
    while i < len(lines):
        m = re.search("([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)", lines[i])
        instruction = Instruction(*[int(m[j]) for j in range(1,5)])
        program.append(instruction)
        i += 1

    return tests, program

def p1(tests, threshold=3):
    count = 0
    for test in tests:
        candidates = 0
        for op in asm:
            r = Registers(test.before)
            asm[op].execute(r, *test.instruction[1:])
            if r == test.after:
                candidates += 1
        if candidates >= threshold:
            count += 1
    return count

def run_program(opmap, program):
    r = Registers()
    for instr in program:
        op = asm[opmap[instr.opcode]]
        op.execute(r, *instr[1:])
    return r[0]

def p2(tests, program):
    solved = {}
    candidates = {}

    for test in tests:
        opcode = test.instruction.opcode

        # We can skip this, we already know it.
        if opcode in solved:
            continue

        # See which instructions this test behaves like
        possibly = set()
        for op in asm:
            r = Registers(test.before)
            asm[op].execute(r, *test.instruction[1:])
            if r == test.after:
                possibly.add(op)

        # Find what's in common with previous runs of this opcode, if any
        if opcode in candidates:
            possibly = set(candidates[opcode]) & possibly

        # Remove any opcodes we've solved, too:
        possibly = possibly - set(solved.values())

        # Success?
        if len(possibly) == 1:
            target = list(possibly)[0]
            logging.info("opcode %d is probably %s", opcode, target)
            solved[opcode] = target

        # Store candidates for future tests to narrow down
        candidates[opcode] = list(possibly)

    return run_program(solved, program)

def aoc16(filename):
    tests, program = load(filename)
    return (p1(tests), p2(tests, program))

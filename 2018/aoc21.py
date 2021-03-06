import asm
import logging

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
    program, ipreg = asm.load(filename)
    sim = asm.Computer(program, n=6, ipreg=ipreg)
    sim.decompile()
    # This really cheats and assumes we all have the same fundamental program ...
    assert(program[7].op == 'seti')
    # And assumes this the parameter of that program ...
    constant = program[7][1]
    # Good luck!
    return decompiled(constant)

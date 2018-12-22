import asm

def p1(sim):
    sim.r.reset()
    return sim.run()

def p2(sim):
    sim.r.reset()
    sim.r[0] = 1
    return sim.run()

def aoc19(filename):
    program, ipreg = asm.load(filename)
    sim = asm.Computer(program, 6, ipreg)
    return (p1(sim), None)

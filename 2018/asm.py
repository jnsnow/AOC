import operator
import logging
from collections import namedtuple

class Registers:
    def __init__(self, initial=None, n=4):
        self.ipreg = None
        self.ip = 0
        if initial:
            self.state = [i for i in initial]
            self.n = len(self.state)
        else:
            self.n = n
            self.reset()

    def name(self, n):
        return chr(ord('A') + n)

    def __str__(self):
        values = []
        values.append("ip(%d)" % self.ip)
        for (i, v) in enumerate(self.state):
            values.append("%c(%d)" % (self.name(i), self.state[v]))
        return ' '.join(values)

    def __getitem__(self, key):
        return self.state[key]

    def __setitem__(self, key, value):
        self.state[key] = value

    def __eq__(self, other):
        return self.state == other.state

    def reset(self):
        self.state = [0] * self.n

    def bind(self, ipreg):
        self.ipreg = ipreg

    def unbind(self):
        self.ipreg = None

# All instructions `INST A B C` take the form: `C:= ?A OP ?B`
# where ?A and ?B are either immediates or a register reference.

ElfProto = namedtuple('ElfProto', ['op', 'fn', 'arity', 'reg', 'imm'])

class ElfOp(ElfProto):
    def format(self):
        if self.arity == 2:
            return "j{ip:02d}: {c:s} = {a} {op:s} {b};"
        if self.arity == 1:
            if self.op is not None:
                return "j{ip:02d}: {c:s} = {op:s}{a};"
            else:
                return "j{ip:02d}: {c:s} = {a};"

    def decompile(self, r, a, b, c, bound=None, verbose=False):
        """Attempts to decompile a single instruction to valid C code.
        It's stateless, so it's definitely wrong in the general case."""
        a_val = a if 0 in self.imm else r.name(a)
        b_val = b if 1 in self.imm else r.name(b)
        c_val = r.name(c)

        if verbose:
            print("/* %s */" % (self.format().format(ip=r.ip, a=a_val, b=b_val,
                                                     c=c_val, op=self.op)))

        # Resolve known values if possible -- we always know the IP register.
        ip_name = r.name(r.ipreg) if r.ipreg else None
        if ip_name == a_val:
            a_val = r.ip
        if ip_name == b_val:
            b_val = r.ip

        # replace assignments to IPREG with jumps, with some caveats.
        if ip_name == c_val:
            try:
                rhs = self.fn(a_val, b_val)
                print("j{:02d}: goto j{:02d};".format(r.ip, rhs + 1))
                return
            except TypeError:
                var = a_val if isinstance(a_val, str) else b_val
                value = a_val if isinstance(a_val, int) else b_val
                # !!! BIG GROSS ASSUMPTIONS !!!
                # Assume that any non-integral A-or-B must be a binary value.
                # Further assume that we will never have two variables.
                print("j{:02d}: if ({:s}) {{".format(r.ip, var))
                print("         goto j{:02d};".format(self.fn(value, 1) + 1))
                print("     } else {")
                print("         goto j{:02d};".format(self.fn(value, 0) + 1))
                print("     }")
                return

        # Print the standard command, otherwise.
        print(self.format().format(ip=r.ip, a=a_val, b=b_val, c=c_val, op=self.op))

    def execute(self, r, a, b, c):
        """Executes the instruction on register set r."""
        a_val = a if 0 in self.imm else r[a]
        b_val = b if 1 in self.imm else r[b]
        r[c] = self.fn(a_val, b_val)

    def trace(self, r, a, b, c):
        """Prints a trace of what execute would do."""
        a_val = a if 0 in self.imm else r[a]
        b_val = b if 1 in self.imm else r[b]
        c_val = r.name(c)
        print(self.format().format(ip=r.ip, a=a_val, b=b_val, c=c_val, op=self.op))

    def register_scan(self, r, a, b, c):
        """Returns the number of the highest register referenced in this instruction."""
        a_reg = -1 if 0 in self.imm else a
        b_reg = -1 if 1 in self.imm else b
        return max(a_reg, b_reg, c)

#                     op    fn           arity reg   imm
asm = { "addr": ElfOp('+',  operator.add,  2, [0,1], []   ),
        "addi": ElfOp('+',  operator.add,  2, [0],   [1]  ),
        "mulr": ElfOp('*',  operator.mul,  2, [0,1], []   ),
        "muli": ElfOp('*',  operator.mul,  2, [0],   [1]  ),
        "banr": ElfOp('&',  operator.and_, 2, [0,1], []   ),
        "bani": ElfOp('&',  operator.and_, 2, [0],   [1]  ),
        "borr": ElfOp('|',  operator.or_,  2, [0,1], []   ),
        "bori": ElfOp('|',  operator.or_,  2, [0],   [1]  ),
        "setr": ElfOp(None, lambda a,b: a, 1, [0],   [1]  ),
        "seti": ElfOp(None, lambda a,b: a, 1, [],    [0,1]),
        "gtir": ElfOp('>',  operator.gt,   2, [1],   [0]  ),
        "gtri": ElfOp('>',  operator.gt,   2, [0],   [1]  ),
        "gtrr": ElfOp('>',  operator.gt,   2, [0,1], []   ),
        "eqir": ElfOp('==', operator.eq,   2, [1],   [0]  ),
        "eqri": ElfOp('==', operator.eq,   2, [0],   [1]  ),
        "eqrr": ElfOp('==', operator.eq,   2, [0,1], []   )}

Instruction = namedtuple('Instruction', ['op', 'a', 'b', 'c'])

class Computer:
    def __init__(self, instructions, n=None, ipreg=None):
        self.instructions = instructions
        if n is None:
            n = self.detect_registers()
        self.r = Registers(n=n)
        if ipreg:
            self.r.bind(ipreg)

    def run(self):
        while True:
            if self.r.ipreg:
                # Copy into aliased register
                self.r[self.r.ipreg] = self.r.ip
            instr = self.instructions[self.r.ip]
            asm[instr.op].execute(self.r, *instr[1:])
            if self.r.ipreg:
                # Copy from aliased register
                self.r.ip = self.r[self.r.ipreg]
            self.r.ip += 1
            if self.r.ip < 0 or self.r.ip >= len(self.instructions):
                return self.r[0]

    def decompile(self):
        """Given a full set of instructions, print out a workable C program."""
        print("#include <stdio.h>")
        print("#include <stdint.h>")
        print("int main(int argc, char *argv[]) {");
        for n,r in enumerate(self.r.state):
            print("uint64_t %s = %dull;" % (self.r.name(n), r))
        for ip, inst in enumerate(self.instructions):
            self.r.ip = ip
            asm[inst.op].decompile(self.r, *inst[1:])
        print(" jend:")
        varstrs = []
        variables = []
        for i in range(len(self.r.state)):
            varstrs.append("%c: 0x%%016lx" % self.r.name(i))
            variables.append("%c" % self.r.name(i))
        fstr = '; '.join(varstrs)
        vstr = ', '.join(variables)
        print("fprintf(stderr, \"%s\\n\", %s);" % (fstr, vstr))
        print("return 0;")
        print("}")

    def detect_registers(self):
        r = max(asm[inst.op].register_scan(None, *inst[1:]) for inst in self.instructions)
        return r + 1

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

    return program, ipreg

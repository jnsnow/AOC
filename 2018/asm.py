import operator
from collections import namedtuple

class Registers:
    def __init__(self, initial=None, n=4):
        if initial:
            self.state = [i for i in initial]
            self.ip = 0
            self.n = len(self.state)
        else:
            self.n = n
            self.reset()

    def __str__(self):
        char = ord('A')
        values = []
        values.append("ip(%d)" % self.ip)
        for (i, v) in enumerate(self.state):
            values.append("%c(%d)" % (char + i, self.state[v]))
        return ' '.join(values)

    def __getitem__(self, key):
        return self.state[key]

    def __setitem__(self, key, value):
        self.state[key] = value

    def __eq__(self, other):
        return self.state == other.state

    def reset(self):
        self.state = [0] * self.n

# All instructions `INST A B C` take the form: `C:= ?A OP ?B`
# where ?A and ?B are either immediates or a register reference.

ElfProto = namedtuple('ElfProto', ['op', 'fn', 'arity', 'reg', 'imm'])

class ElfOp(ElfProto):
    def format(self):
        if self.arity == 2:
            return "{ip:02d}: {c:s} = {b} {op:s} {a}"
        if self.arity == 1:
            if self.op is not None:
                return "{ip:02d}: {c:s} = {op:s}{a}"
            else:
                return "{ip:02d}: {c:s} = {a}"

    def decompile(self, r, a, b, c):
        a_val = a if 0 in self.imm else chr(ord('A') + a)
        b_val = b if 1 in self.imm else chr(ord('A') + b)
        c_val = chr(ord('A') + c)
        print(self.format().format(ip=r.ip, a=a_val, b=b_val, c=c_val, op=self.op))

    def execute(self, r, a, b, c):
        a_val = a if 0 in self.imm else r[a]
        b_val = b if 1 in self.imm else r[b]
        r[c] = self.fn(a_val, b_val)

    def trace(self, r, a, b, c):
        a_val = a if 0 in self.imm else r[a]
        b_val = b if 1 in self.imm else r[b]
        c_val = chr(ord('A') + c)
        print(self.format().format(ip=r.ip, a=a_val, b=b_val, c=c_val, op=self.op))

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


class Operations:
    _table = {}

    def register_op(table):
        def inner(fn):
            table[fn.__name__] = fn
            return fn
        return inner

    @staticmethod
    @register_op(_table)
    def addr(regs, args):
        regs[args[2]] = regs[args[0]] + regs[args[1]]

    @staticmethod
    @register_op(_table)
    def addi(regs, args):
        regs[args[2]] = regs[args[0]] + args[1]

    @staticmethod
    @register_op(_table)
    def mulr(regs, args):
        regs[args[2]] = regs[args[0]] * regs[args[1]]

    @staticmethod
    @register_op(_table)
    def muli(regs, args):
        regs[args[2]] = regs[args[0]] * args[1]

    @staticmethod
    @register_op(_table)
    def banr(regs, args):
        regs[args[2]] = regs[args[0]] & regs[args[1]]

    @staticmethod
    @register_op(_table)
    def bani(regs, args):
        regs[args[2]] = regs[args[0]] & args[1]

    @staticmethod
    @register_op(_table)
    def borr(regs, args):
        regs[args[2]] = regs[args[0]] | regs[args[1]]

    @staticmethod
    @register_op(_table)
    def bori(regs, args):
        regs[args[2]] = regs[args[0]] | args[1]

    @staticmethod
    @register_op(_table)
    def setr(regs, args):
        regs[args[2]] = regs[args[0]]

    @staticmethod
    @register_op(_table)
    def seti(regs, args):
        regs[args[2]] = args[0]

    @staticmethod
    @register_op(_table)
    def gtir(regs, args):
        regs[args[2]] = int(args[0] > regs[args[1]])

    @staticmethod
    @register_op(_table)
    def gtri(regs, args):
        regs[args[2]] = int(regs[args[0]] > args[1])

    @staticmethod
    @register_op(_table)
    def gtrr(regs, args):
        regs[args[2]] = int(regs[args[0]] > regs[args[1]])

    @staticmethod
    @register_op(_table)
    def eqir(regs, args):
        regs[args[2]] = int(args[0] == regs[args[1]])

    @staticmethod
    @register_op(_table)
    def eqri(regs, args):
        regs[args[2]] = int(regs[args[0]] == args[1])

    @staticmethod
    @register_op(_table)
    def eqrr(regs, args):
        regs[args[2]] = int(regs[args[0]] == regs[args[1]])

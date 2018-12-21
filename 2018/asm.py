class Registers:
    def __init__(self, initial=None, n=4):
        if initial:
            self.state = [i for i in initial]
            self.n = len(self.state)
        else:
            self.n = n
            self.reset()

    def __str__(self):
        char = ord('A')
        values = []
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

# addr $C := $A + $B
# addi $C := $A +  B
# mulr $C := $A + $B
# muli $C := $A +  B
# banr $C := $A + $B
# bani $C := $A +  B
# borr $C := $A | $B
# bori $C := $A |  B
# setr $C := $A
# seti $C :=  A
# gtir $C :=  A > $B
# gtri $C := $A >  B
# gtrr $C := $A > $B
# eqir $C :=  A == $B
# eqri $C := $A ==  B
# eqrr $C := $A == $B

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

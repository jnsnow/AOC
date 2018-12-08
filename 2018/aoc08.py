#!/usr/bin/python3

class node:
    def __init__(self):
        self.children = []
        self.metadata = []

    def read(self, seq):
        numchildren = seq.pop(0)
        numdata = seq.pop(0)
        for i in range(numchildren):
            self.children.append(node.from_read(seq))
        for i in range(numdata):
            self.metadata.append(seq.pop(0))
        return self

    @staticmethod
    def from_read(seq):
        return node().read(seq)

    def p1_value(self):
        return sum(self.metadata) + sum([c.p1_value() for c in self.children])

    def p2_value(self):
        if not self.children:
            return sum(self.metadata)
        childsum = 0
        for m in self.metadata:
            if m == 0:
                continue
            m -= 1
            if m < len(self.children):
                childsum += self.children[m].p2_value()
        return childsum

def aoc08(filename):
    f = open(filename, "r")
    seq = f.read()
    seq = [int(x) for x in seq.strip().split(' ')]
    root = node.from_read(seq)
    return [root.p1_value(), root.p2_value()]

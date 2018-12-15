import itertools

def p1(lines):
    doubles_count = 0
    triples_count = 0
    for line in lines:
        last = None
        count = 0
        has_double = False
        has_triple = False
        line = sorted(line.strip()) + ['\n']
        for letter in line:
            if letter == last:
                count += 1
            else:
                has_double = True if count == 2 else has_double
                has_triple = True if count == 3 else has_triple
                last = letter
                count = 1
        doubles_count += (1 * has_double)
        triples_count += (1 * has_triple)
    return doubles_count * triples_count

def hamming2(s1, s2):
    """Calculate the Hamming distance between two bit strings"""
    assert len(s1) == len(s2)
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def p2(lines):
    for a, b in itertools.combinations(lines, 2):
        if hamming2(a, b) == 1:
            print("%s ~= %s" % (a, b))
            answ = ''.join([a for a, b in zip(a, b) if a == b])
            return answ

def aoc02(filename):
    f = open(filename, 'r')
    lines = [s.strip() for s in f]
    return [p1(lines), p2(lines)]

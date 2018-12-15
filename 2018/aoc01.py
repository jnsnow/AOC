def p1(freqs):
    return sum(freqs)

def p2(freqs):
    freq = 0
    freqmap = {}
    while True:
        for adjustment in freqs:
            freq += adjustment
            if freq in freqmap:
                return freq
            freqmap[freq] = True

def aoc01(filename):
    f = open(filename, "r")
    freqs = [int(line.strip()) for line in f]
    return [p1(freqs), p2(freqs)]





import re
import logging

def p1(filename):
    f = open(filename, "r")
    line = f.readline()
    players = int(re.search("([0-9]+) players;", line)[1])
    marbles = int(re.search("([0-9]+) points", line)[1])
    scores = [0] * players
    ring = [0]
    n = 0
    currpos = 0
    while n < marbles:
        for p in range(players):
            if n >= marbles:
                break
            insertpos = ((currpos + 1) % len(ring)) + 1
            n += 1
            if n % 23:
                ring.insert(insertpos, n)
                currpos = insertpos
            else:
                scores[p] += n
                removepos = (currpos - 7) % len(ring)
                scores[p] += ring.pop(removepos)
                currpos = removepos % len(ring)
            #logging.info("[%d] %s", (p + 1), " ".join([str(x) for x in ring]))
    return max(scores)

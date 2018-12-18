letters = [chr(x) for x in range(ord('a'), ord('z') + 1)]

def collapse(line):
    while True:
        l = len(line)
        for letter in letters:
            line = line.replace("%c%c" % (letter, letter.swapcase()), "")
            line = line.replace("%c%c" % (letter.swapcase(), letter), "")
        if len(line) == l:
            return len(line)

def p1(line):
    return collapse(line)

def p2(line):
    baseline = line
    scores = {}
    for char in letters:
        line = line.replace(char, "")
        line = line.replace(char.swapcase(), "")
        scores[char] = collapse(line)
        line = baseline
    return min(scores.values())

def aoc05(filename):
    f = open("/home/nago/Documents/input5.txt", "r")
    line = f.readline().strip()
    return [p1(line), p2(line)]

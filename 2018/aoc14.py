def digits(num):
    return [int(d) for d in list(str(num))]

def aoc14(input, seeddata=[3, 7], elves=2):
    scores = [] + seeddata
    pointers = [x for x in range(elves)]
    inputlst = digits(input)
    ll = len(inputlst)
    # Each score is limited to a single decimal digit,
    # so the maximum sum for n elves is (n*9).
    maxsum = len(digits(9*elves))
    found = False
    while not (len(scores) >= (input + 10) and found):
        tmp_scores = [scores[pointers[x]] for x in range(elves)]
        scores.extend(digits(sum(tmp_scores)))
        pointers = [(pointers[i] + scores[pointers[i]] + 1) % len(scores) for i in range(elves)]
        if (len(scores) < len(inputlst)) or found:
            continue
        # This unholy slice looks at [-6:None], [-7:-1], ...
        # (and [-8:-2] and beyond if necessary, based on maxsum.)
        for i in range(maxsum):
            if inputlst == scores[((-ll) - i):(None if i == 0 else 0 - i)]:
                p2_answ = len(scores) - ll - i
                found = True
                break
    p1_answ = ''.join([str(x) for x in scores[input:input+10]])
    return [p1_answ, p2_answ]

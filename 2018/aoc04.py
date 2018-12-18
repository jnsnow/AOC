import re

def common(filename):
    f = open(filename, "r")
    slines = sorted(f.readlines())
    sleepcnt = {}
    sleepmap = {}
    sleepstart = None
    sleepstop = None
    for line in slines:
        res = re.search(':([0-9]+)\](?: Guard #([0-9]+))? (begins shift|falls asleep|wakes up)', line)
        minute = int(res[1])
        event = res[3]
        if event == 'begins shift':
            currguard = int(res[2])
            sleepstart = None
            sleepstop = None
        elif event == 'falls asleep':
            sleepstart = minute
        elif event == 'wakes up':
            sleepstop = minute
            assert(sleepstart is not None)
            sleepcnt[currguard] = sleepcnt.get(currguard, 0) + (sleepstop - sleepstart)
            if currguard not in sleepmap:
                sleepmap[currguard] = {}
            for i in range(sleepstart, sleepstop):
                sleepmap[currguard][i] = sleepmap[currguard].get(i, 0) + 1
            sleepstart = None
    return sleepcnt, sleepmap

def p1(sleepcnt, sleepmap):
    guard, _ = max(sleepcnt.items(), key=lambda x: x[1])
    minute, _ = max(sleepmap[guard].items(), key=lambda x: x[1])
    return guard * minute

def p2(sleepcnt, sleepmap):
    # map of {guard: times_asleep_at_one_minute}
    minutemap = {k: max(v.values()) for k,v in sleepmap.items()}
    # guard who is most consistently asleep at any one time
    guard, _ = max(minutemap.items(), key=lambda x: x[1])
    minute, _ = max(sleepmap[guard].items(), key=lambda x: x[1])
    return guard * minute

def aoc04(filename):
    sleepcnt, sleepmap = common(filename)
    return [p1(sleepcnt, sleepmap), p2(sleepcnt, sleepmap)]

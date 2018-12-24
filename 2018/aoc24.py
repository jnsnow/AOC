import re
import logging
from itertools import count

class War:
    def __init__(self, fstream):
        self.armies = []
        while True:
            army = Army(fstream)
            if army.name:
                self.armies.append(army)
            else:
                break
        self.counter = count(0)

    def target_selection(self, round_):
        order = self.armies[0].groups + self.armies[1].groups
        order = sorted(order,
                       key=lambda g: (-g.effective_power(), -g.initiative))
        for group in order:
            group.select_target([other for other in order
                                 if group.army != other.army
                                 and other.last_round_attacked != round_],
                                round_)

    def attack(self):
        order = self.armies[0].groups + self.armies[1].groups
        order = sorted(order, key=lambda g: -g.initiative)
        for group in order:
            group.do_attack()

    def fight(self):
        round_ = next(self.counter)
        self.target_selection(round_)
        self.attack()
        for army in self.armies:
            army.cull_dead()

    def run(self):
        while True:
            reports = [army.report() for army in self.armies]
            self.fight()
            if reports == [army.report() for army in self.armies]:
                logging.warning("Stalemate detected")
                return None, None
            if not (self.armies[0].groups and self.armies[1].groups):
                break
        army = self.armies[0]
        if not army.groups:
            army = self.armies[1]
        return army.name, army.report()


class Army:
    def __init__(self, f):
        self.name = f.readline().split(':')[0]
        self.groups = []
        for line in f:
            if not line.strip():
                break
            immunities = []
            weaknesses = []
            m = re.match(r'(?P<units>\d+) units each with (?P<hp>\d+) hit points (?P<affinities>\(.+?\) )?with an attack that does (?P<pwr>\d+) (?P<atyp>.+?) damage at initiative (?P<init>\d+)', line)
            if m['affinities']:
                m2 = re.match(r'\((.+?)\)', m['affinities'])
                for affinity in m2[1].split(';'):
                    if 'immune' in affinity:
                        affinity = affinity.replace("immune to ", "")
                        immunities = [imm.strip() for imm in affinity.split(',')]
                    if 'weak to' in affinity:
                        affinity = affinity.replace("weak to ", "")
                        weaknesses = [wkns.strip() for wkns in affinity.split(',')]
            g = Group(int(m['units']), int(m['hp']), int(m['pwr']), m['atyp'], int(m['init']), weaknesses, immunities)
            g.army = self
            self.groups.append(g)

    def cull_dead(self):
        self.groups = [g for g in self.groups if g.units > 0]

    def report(self):
        return sum([g.units for g in self.groups if g.units > 0])

    def boost(self, n):
        for g in self.groups:
            g.attack_power += n


class Group:
    def __init__(self, units, hp, attack_power, attack_type,
                 initiative, weaknesses=None, immunities=None):
        self.army = None
        self.units = units
        self.hp = hp
        self.attack_power = attack_power
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = weaknesses or []
        self.immunities = immunities or []
        self.last_round_attacked = -1
        self.targeting = None

    def __repr__(self):
        fmt = "Group(%d, %d, %d, %s, %d, weaknesses=%s, immunities=%s)"
        return fmt % (self.units, self.hp, self.attack_power, self.attack_type,
                      self.initiative, self.weaknesses, self.immunities)

    def effective_power(self):
        return self.units * self.attack_power

    def attack_damage(self, units, attack_type, attack_power):
        if attack_type in self.immunities:
            return 0
        elif attack_type in self.weaknesses:
            return attack_power * 2 * units
        else:
            return attack_power * units

    def damage(self, units, attack_type, attack_power):
        dam = self.attack_damage(units, attack_type, attack_power)
        # is this...
        loss = int(dam/self.hp)
        loss = min(loss, self.units)
        logging.debug("group %d took %d dam against %d hp to lose %d units",
                      self.initiative, dam, self.hp, loss)
        self.units = self.units - loss

    def do_attack(self):
        if self.targeting:
            logging.info("Army %s Group %d attacking Army %s Group %d",
                         self.army.name, self.initiative,
                         self.targeting.army.name, self.targeting.initiative)
            self.targeting.damage(self.units, self.attack_type, self.attack_power)
            self.targeting = None
        else:
            logging.info("Group %d Army %s had nobody to attack",
                         self.initiative, self.army.name)

    def select_target(self, others, round_):
        # 1. by Attack Damage, Desc
        # 2. by Effective Power, Desc
        # 3. by Initiative, Desc.
        targets = sorted([(o,
                           (-o.attack_damage(self.units, self.attack_type, self.attack_power),
                            -o.effective_power(),
                            -o.initiative))
                          for o in others],
                         key=lambda pair: pair[1])
        logging.debug("%d candidate targets", len(targets))
        while targets:
            candidate = targets.pop(0)
            if -candidate[1][0] > 0:
                self.targeting = candidate[0]
                self.targeting.last_round_attacked = round_
                logging.debug("Group %d predicts %d damage against %d",
                              self.initiative,
                              -candidate[1][0],
                              self.targeting.initiative)
                break

def p1(filename):
    f = open(filename, 'r')
    w = War(f)
    _, answ = w.run()
    return answ

def p2(filename):
    for i in count(1):
        f = open(filename, 'r')
        w = War(f)
        for army in w.armies:
            if army.name == 'Immune System':
                w.armies[0].boost(i)
        name, answ = w.run()
        if name == 'Immune System':
            return answ

def aoc24(filename):
    return (p1(filename), p2(filename))

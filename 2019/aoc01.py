#!/usr/bin/env python3

def fuel_needed(mass):
    return max(0, int(mass / 3) - 2)

def fuel_needed_inclusive(mass):
    if mass <= 0:
        return 0
    fuel = fuel_needed(mass)
    return fuel + fuel_needed_inclusive(fuel)

def tally(masses, callback):
    return sum([callback(mass) for mass in masses])

def p1(masses):
    return tally(masses, fuel_needed)

def p2(masses):
    return tally(masses, fuel_needed_inclusive)

def aoc01(filename):
    with open(filename, "r") as inputs:
        masses = [int(line) for line in inputs]
    return [p1(masses), p2(masses)]

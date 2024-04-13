#!/usr/bin/env python3

import re

# Record gear coordinates and their adjacent part numbers in a dict.
# Each key is a tuple of the gear coordinates, the value is a list of adjacent
# part numbers.
gears_numbers = dict()

number = re.compile(r"\d+")
gear = re.compile(r"\*")

# Given the position of a number, look around to find a gear and associate the
# part number with it.
def find_gears(line, start, end, number):
    #print (f'Looking around {number} at line {line} ({start} -> {end})')
    # Look at the line above
    for line in range(line -1, line + 2):
        for column in range(start - 1, end + 1):
            coord = (line, column)
            if coord in gears_numbers:
                gears_numbers[coord].append(number)

# Find the gears first
with open('data-1.txt', 'r') as content:
    for (line_number, line) in enumerate(content):
        line = line.splitlines()[0]

        for g in gear.finditer(line):
            gears_numbers[(line_number, g.start())] = []

# And then the numbers
with open('data-1.txt', 'r') as content:
    for (line_number, line) in enumerate(content):
        line = line.splitlines()[0]

        for n in number.finditer(line):
            find_gears(line_number, n.start(), n.end(), int(n[0]))

gear_ratios = [numbers[0] * numbers[1] for numbers in gears_numbers.values() if
               len(numbers) == 2]

print('Sum of the part numbers:', sum(gear_ratios))

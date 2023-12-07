#!/usr/bin/env python3

import re

# Coordinates adjacent to a symbol as (line, column) tuples
symbols_coordinates = set()
# Coordinates of numbers as (line, start, end, number) tuples
numbers_coordinates = []
# Part numbers
part_numbers = []

number = re.compile(r"\d+")
symbol = re.compile(r"[^.0-9]")

def get_surrounding_coords(line, column):
    coords = [
        (line - 1, column - 1), (line - 1, column), (line - 1, column + 1),
        (line, column - 1), (line, column), (line, column + 1),
        (line + 1, column - 1), (line + 1, column), (line + 1, column + 1),
    ]
    
    return coords

with open('data-1.txt', 'r') as content:
    for (line_number, line) in enumerate(content):
        line = line.splitlines()[0]

        for n in number.finditer(line):
            numbers_coordinates.append((line_number, n.start(), n.end(),
                                        int(n[0])))

        for s in symbol.finditer(line):
            symbols_coordinates.update(get_surrounding_coords(line_number,
                                                              s.start()))

for n in numbers_coordinates:
    (line, start, end, number) = n
    for pos in range(start, end):
        if (line, pos) in symbols_coordinates:
            part_numbers.append(number)
            break

#print(numbers_coordinates)
#print(symbols_coordinates)
#print(part_numbers)
print('Sum of the part numbers:', sum(part_numbers))

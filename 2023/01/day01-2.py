#!/usr/bin/env python3

numbers = [
    'zero', 'one', 'two', 'three', 'four',
    'five', 'six', 'seven', 'eight', 'nine',
]
numbers = {n: i for (i, n) in enumerate(numbers)}

numbers_dict = {}
for n in numbers:
    if n[0] not in numbers_dict:
        numbers_dict[n[0]] = []
    numbers_dict[n[0]].append(n)

def find_first_number(line: str) -> str:
    for i, c in enumerate(line):
        if c.isdigit():
            return c
        elif (number := find_number(line, i, c)) is not None:
            return str(number)

    return 0

def find_last_number(line: str) -> str:
    for i, c in enumerate(reversed(line)):
        if c.isdigit():
            return c
        elif (number := find_number(line, len(line) - i - 1, c)) is not None:
            return str(number)

    return 0

def find_number(line: str, index: int, char: str) -> int:
    try:
        for number in numbers_dict[char]:
            if line.find(number, index, index + len(number)) != -1:
                return numbers[number]
    except KeyError:
        return None

    return None

calibration = []

with open("calibration-2.txt", 'r') as content:
    for line in content:
        first, last = 0, 0
        first = find_first_number(line)
        last = find_last_number(line)

        calibration.append(int(first + last))

print('Calibration:', sum(calibration))

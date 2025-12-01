import sys
import unittest
from functools import reduce

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    grand_total = data_from_file(filename, analyse_worksheet)
    print(f"Grand total: {grand_total}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def data_from_file(filename, cb):
    try:
        with open(filename, 'r') as file:
            return cb(file)

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

def analyse_worksheet(file):
    grand_total = 0
    max_length = 0
    lines = []
    operators = []

    for line in file:
        if line[0] in ('+', '*'):
            operators = line.strip().split()
        else:
            line = [c.strip() for c in line]
            lines.append(line)

            max_length = max(max_length, len(line))

    numbers = get_numbers(lines, max_length)
    for i, op in enumerate(operators):
        values = next(numbers)

        if op == '+':
            grand_total += sum(values)
        elif op == '*':
            grand_total += reduce(lambda x, y: x*y, values, 1)

    return grand_total

def get_numbers(lines, max_length):
    column = 0 # Character column, not data column

    while column < max_length:
        numbers = []
        while any(digits := [line[column] if column < len(line) else '' for line in lines]):
            numbers.append(int(''.join(digits)))
            column += 1

        yield numbers

        column += 1

class TestWorksheet(unittest.TestCase):
    def test_grand_total(self):
        grand_total = data_from_file('example.txt', analyse_worksheet)
        self.assertEqual(grand_total, 3263827)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

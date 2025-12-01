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
    lines = []
    operators = []

    for line in file:
        if line[0] in ('+', '*'):
            operators = line.strip().split()
        else:
            lines.append(list(map(int, line.strip().split())))

    for i, op in enumerate(operators):
        if op == '+':
            grand_total += sum([line[i] for line in lines])
        elif op == '*':
            grand_total += reduce(
                lambda x, y: x*y,
                [line[i] for line in lines],
                1
            )

    return grand_total

class TestWorksheet(unittest.TestCase):
    def test_grand_total(self):
        grand_total = data_from_file('example.txt', analyse_worksheet)
        self.assertEqual(grand_total, 4277556)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

import sys
import unittest

from functools import reduce
from itertools import product

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    values = data_from_file(filename, analyze_calibration)
    print(f"Sum of possibly correct calibrations: {sum(values)}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def analyze_calibration(file):
    correct_values = []

    for line in file:
        (value, numbers) = line.split(':')
        numbers = [n for n in map(int, numbers.split())]
        value = int(value)

        """ Get the number of possible combinations of + and * """
        operations = product("+*", repeat=len(numbers)-1)
        for sequence in operations:
            result = reduce(compute_calibration(sequence), numbers)
            if result == value:
                correct_values.append(value)
                break

    return correct_values


def compute_calibration(operations):
    def operator(operations):
        for op in operations:
            yield op

    generator = operator(operations)

    def compute(x, y):
        op = next(generator)
        match op:
            case '+':
                return x + y
            case '*':
                return x * y

    return compute

def data_from_file(filename, cb):
    try:
        with open(filename, 'r') as file:
            return cb(file)

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

class TestCalibration(unittest.TestCase):
    values = 0

    @classmethod
    def setUpClass(cls):
        cls.values = data_from_file('example.txt', analyze_calibration)

    def test_calibrations(self):
        self.assertEqual(sum(self.values), 3749)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

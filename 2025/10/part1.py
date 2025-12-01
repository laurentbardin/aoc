import sys
import unittest

from itertools import combinations_with_replacement
from functools import reduce

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    count = data_from_file(filename, count_button_presses)
    print(f"Minimum button presses: {count}")

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

def count_button_presses(file):
    machines = []

    for line in file:
        elements = line.strip().split()
        machine = {'buttons': []}
        for e in elements:
            match e[0]:
                case '[':
                    lights = e[1:-1]
                    machine['lights'] = lights
                    machine['target'] = get_target(lights)
                case '(':
                    machine['buttons'].append(get_button(e[1:-1]))

        machines.append(machine)

    button_presses = 0
    for machine in machines:
        button_presses += solve(machine)

    return button_presses

def get_target(diagram):
    target = [2**i if c == '#' else 0 for i, c in enumerate(diagram)]
    return sum(target)

def get_button(button):
    bits = map(int, button.split(','))
    return sum([2**bit for bit in bits])

def solve(machine):
    presses = 1
    # Define a reasonable, yet arbitrary, limit to the number of presses
    while presses <= len(machine['buttons']) * 2:
        for combination in combinations_with_replacement(machine['buttons'], presses):
            result = reduce(lambda x, y: x^y, combination, 0)
            if result == machine['target']:
                return presses
        presses += 1
    else:
        print(f'Could not solve machine {machine['lights']} '
              '(try increasing the maximum number of presses')

    return 0

class TestButtonPresses(unittest.TestCase):
    def test_button_presses(self):
        presses = data_from_file('example.txt', count_button_presses)
        self.assertEqual(presses, 7)

    def test_target_from_lights(self):
        lights = '.#.##..#'
        self.assertEqual(get_target(lights), 154)

        lights = '........'
        self.assertEqual(get_target(lights), 0)

        lights = '########'
        self.assertEqual(get_target(lights), 255)

    def test_buttons(self):
        button = '0,1'
        self.assertEqual(get_button(button), 3)

        button = '2,7'
        self.assertEqual(get_button(button), 132)

        button = '3,5,6'
        self.assertEqual(get_button(button), 104)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

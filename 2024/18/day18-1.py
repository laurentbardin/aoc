import sys
import unittest

import a_star

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    steps = data_from_file(filename, analyze_memory(70, 70, 1024))
    print(f"Smallest number of steps to the exit: {steps}")

def analyze_memory(grid_width, grid_height, size):
    grid = [[' '] * (grid_width + 1) for _ in range(grid_height + 1)]

    def callback(file):
        for line, byte in list(enumerate(file))[:size]:
            x, y = (n for n in map(int, byte.splitlines()[0].split(',')))
            grid[y][x] = '#'

        _, path = a_star.solve(grid, (0, 0), (grid_width, grid_height))

        # The nodes list include the starting position, so we have to substract
        # 1 to get the number of steps
        return len(path) - 1

    return callback

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

class TestDistances(unittest.TestCase):
    def test_path(self):
        length = data_from_file('example.txt', analyze_memory(6, 6, 12))
        self.assertEqual(length, 22)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

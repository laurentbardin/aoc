import sys
import unittest

import a_star

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    byte = data_from_file(filename, analyze_memory(70, 70, 1024))
    print(f"First byte to prevent the exit from being reachable: {byte}")

def analyze_memory(grid_width, grid_height, start):
    grid = [[' '] * (grid_width + 1) for _ in range(grid_height + 1)]

    def callback(file):
        """
        This is a brute-force solution where we search for a path with each new
        byte after the starting position.
        TODO for a rainy day: implement a divide and conquer algorithm.
        """
        bytes = list(enumerate(file))
        for line, byte in bytes:
            x, y = map(int, byte.splitlines()[0].split(','))
            grid[y][x] = '#'

            if line >= start:
                _, path = a_star.solve(grid, (0, 0), (grid_width, grid_height))
                if path is None:
                    return f"{x},{y}"

        return "None"

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
        byte = data_from_file('example.txt', analyze_memory(6, 6, 12))
        self.assertEqual(byte, "6,1")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

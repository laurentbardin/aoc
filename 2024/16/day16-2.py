import sys
import unittest

import a_star

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    best_nodes = data_from_file(filename, analyze_map)

    print(f"Number of tiles part of at least one best path: {best_nodes}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def count_nodes(paths):
    best_nodes = set()
    for path in paths:
        best_nodes.update(path.keys())

    return best_nodes

def analyze_map(file):
    start = ()
    dest = ()
    grid = []

    for (n, line) in enumerate(file):
        grid.append(line.splitlines()[0])
        if 'E' in line:
            dest = (line.index('E'), n)
        elif 'S' in line:
            start = (line.index('S'), n)

    assert len(start) > 0
    assert len(dest) > 0

    _, paths = a_star.solve_multiple(grid, start, dest)

    return len(count_nodes(paths))

def data_from_file(filename, cb):
    try:
        with open(filename, 'r') as file:
            return cb(file)

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

class TestTopography(unittest.TestCase):

    def test_score_1(self):
        best_nodes = data_from_file('example-1.txt', analyze_map)
        self.assertEqual(best_nodes, 45)

    def test_score_2(self):
        best_nodes = data_from_file('example-2.txt', analyze_map)
        self.assertEqual(best_nodes, 64)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

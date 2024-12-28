import sys
import unittest

import a_star

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    score = data_from_file(filename, analyze_map)
    print(f"Lowest score: {score}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

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

    score = a_star.solve(grid, start, dest)
    return score

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
        score = data_from_file('example-1.txt', analyze_map)
        self.assertEqual(score, 7036)

    def test_score_2(self):
        score = data_from_file('example-2.txt', analyze_map)
        self.assertEqual(score, 11048)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

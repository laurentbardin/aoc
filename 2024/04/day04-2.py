import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    total = data_from_file(filename, analyze_puzzle)
    print(f"X-MAS Total: {total}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def analyze_puzzle(file):
    lines = []

    for (_, data) in enumerate(file):
        lines.append(data)

    return find_xmas(lines)

def find_xmas(lines):
    xmas = 0

    for (line, content) in enumerate(lines):
        for pos, c in enumerate(content):
            if c == 'A':
                xmas += search_xmas(pos, line, lines)

    return xmas

def search_xmas(x, y, lines):
    if x < 1 or x > len(lines[y]) - 2:
        return 0
    if y < 1 or y > len(lines) - 2:
        return 0

    branches = 0
    if (lines[y-1][x-1] == 'M' and lines[y+1][x+1] == 'S') or (lines[y-1][x-1] == 'S' and lines[y+1][x+1] == 'M'):
        branches += 1
    if (lines[y-1][x+1] == 'M' and lines[y+1][x-1] == 'S') or (lines[y-1][x+1] == 'S' and lines[y+1][x-1] == 'M'):
        branches += 1

    return 1 if branches == 2 else 0

def data_from_file(filename, cb):
    try:
        with open(filename, 'r') as file:
            return cb(file)

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

class TestPuzzle(unittest.TestCase):
    xmas = 0

    @classmethod
    def setUpClass(cls):
        cls.xmas = data_from_file('example.txt', analyze_puzzle)

    def test_reports(self):
        self.assertEqual(self.xmas, 9)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

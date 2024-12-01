import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    total = data_from_file(filename, analyze_puzzle)
    print(f"XMAS Total: {total}")

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
            if c == 'X':
                xmas += search_north(pos, line, lines)
                xmas += search_east(pos, line, lines)
                xmas += search_south(pos, line, lines)
                xmas += search_west(pos, line, lines)
                xmas += search_neast(pos, line, lines)
                xmas += search_nwest(pos, line, lines)
                xmas += search_seast(pos, line, lines)
                xmas += search_swest(pos, line, lines)

    return xmas

def search_north(x, y, lines):
    if y < 3:
        return 0
    if lines[y-1][x] == 'M' and lines[y-2][x] == 'A' and lines[y-3][x] == 'S':
        return 1
    return 0

def search_east(x, y, lines):
    if x > len(lines[y]) - 1 - 3:
        return 0
    if lines[y][x+1] == 'M' and lines[y][x+2] == 'A' and lines[y][x+3] == 'S':
        return 1
    return 0

def search_south(x, y, lines):
    if y > len(lines) - 1 - 3:
        return 0
    if lines[y+1][x] == 'M' and lines[y+2][x] == 'A' and lines[y+3][x] == 'S':
        return 1
    return 0

def search_west(x, y, lines):
    if x < 3:
        return 0
    if lines[y][x-1] == 'M' and lines[y][x-2] == 'A' and lines[y][x-3] == 'S':
        return 1
    return 0

def search_neast(x, y, lines):
    if y < 3 or x > len(lines[y]) - 1 - 3:
        return 0
    if lines[y-1][x+1] == 'M' and lines[y-2][x+2] == 'A' and lines[y-3][x+3] == 'S':
        return 1
    return 0

def search_nwest(x, y, lines):
    if y < 3 or x < 3:
        return 0
    if lines[y-1][x-1] == 'M' and lines[y-2][x-2] == 'A' and lines[y-3][x-3] == 'S':
        return 1
    return 0

def search_seast(x, y, lines):
    if x > len(lines[y]) - 1 - 3 or y > len(lines) - 1 - 3:
        return 0
    if lines[y+1][x+1] == 'M' and lines[y+2][x+2] == 'A' and lines[y+3][x+3] == 'S':
        return 1
    return 0

def search_swest(x, y, lines):
    if y > len(lines) - 1 - 3 or x < 3:
        return 0
    if lines[y+1][x-1] == 'M' and lines[y+2][x-2] == 'A' and lines[y+3][x-3] == 'S':
        return 1
    return 0

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
        self.assertEqual(self.xmas, 18)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

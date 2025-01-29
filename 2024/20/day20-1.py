import sys
import unittest

from a_star import solve

SAVINGS_THRESHOLD = 100

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    shortcuts = data_from_file(filename, analyze_cpu)
    print(f"Number of shortcuts saving 100+ picoseconds: {shortcuts}")

def analyze_cpu(file):
    start = ()
    end = ()
    grid = []
    duration = 0
    for y, line in enumerate(file):
        line = line.splitlines()[0]
        grid.append(line)
        if 'S' in line:
            start = (line.find('S'), y)

        if 'E' in line:
            end = (line.find('E'), y)

        duration += line.count('.')

    # Each moves costs 1 picosecond, so add one to reach the end
    duration += 1

    _, path = solve(grid, start, end)
    assert duration == len(path) - 1

    shortcuts = find_shortcuts(grid)

    # Map time saved to number of shortcuts
    timings = dict()
    for wall, neighbours in shortcuts.items():
        n1, n2 = neighbours
        assert n1 in path
        assert n2 in path

        bypassed = abs(path.index(n1) - path.index(n2)) - 1
        saved_time = bypassed - 1
        if saved_time not in timings:
            timings[saved_time] = 0

        timings[saved_time] += 1

    #for t, s in timings.items():
    #    print(f"{s} shortcut(s) save {t} picosecond(s)")

    return sum([s for t, s in timings.items() if t >= SAVINGS_THRESHOLD])

def find_shortcuts(grid):
    """
    Find potential shortcuts: walls separating two track nodes, either
    vertically or horizontally.
    """
    shortcuts = dict()
    width = len(grid[0])
    height = len(grid)

    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if 0 < y < height - 1 and 0 < x < width - 1 and char == '#':
                if (grid[y-1][x] in '.ES' and grid[y+1][x] in '.ES'):
                    shortcuts[(x, y)] = ((x, y-1), (x, y+1))
                elif (grid[y][x-1] in '.ES' and grid[y][x+1] in '.ES'):
                    shortcuts[(x, y)] = ((x-1, y), (x+1, y))

    return shortcuts

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

class TestShortcuts(unittest.TestCase):
    def test_shortcuts(self):
        global SAVINGS_THRESHOLD

        SAVINGS_THRESHOLD = 10
        shortcuts = data_from_file('example.txt', analyze_cpu)
        self.assertEqual(shortcuts, 10)

        SAVINGS_THRESHOLD = 20
        shortcuts = data_from_file('example.txt', analyze_cpu)
        self.assertEqual(shortcuts, 5)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

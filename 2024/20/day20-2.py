import sys
import unittest

from a_star import solve
from node import Node

SAVINGS_THRESHOLD = 100
MAX_CHEAT_DURATION = 20

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
    for line, data in enumerate(file):
        data = data.splitlines()[0]
        grid.append(data)
        if 'S' in data:
            start = (data.find('S'), line)

        if 'E' in data:
            end = (data.find('E'), line)

        duration += data.count('.')

    # Each moves costs 1 picosecond, so add one to reach the end
    duration += 1

    _, path = solve(grid, start, end)
    assert duration == len(path) - 1

    valuable_shartcuts = 0
    for i in range(len(path)):
        ref_node = Node(path[i])
        #if i % 100 == 0:
        #    print(f"Checking node #{i}/{len(path)}")
        for j, pos in enumerate(path):
            # Skip already checked pairs
            if j <= i:
                continue

            node = Node(pos)
            dist = ref_node.manhattan(node)

            # Skip nodes which are too far to be reached in at most
            # MAX_CHEAT_DURATION picoseconds
            if dist > MAX_CHEAT_DURATION:
                continue

            saved_time = j - i - dist
            # Skip nodes not reachable faster using a shortcut, or whose
            # improvement is below the required threshold
            if saved_time <= 0 or saved_time < SAVINGS_THRESHOLD:
                continue

            valuable_shartcuts += 1

    #for t, s in timings.items():
    #    print(f"{s} shortcut(s) save {t} picosecond(s)")

    return valuable_shartcuts

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

        SAVINGS_THRESHOLD = 50
        shortcuts = data_from_file('example.txt', analyze_cpu)
        self.assertEqual(shortcuts, 285)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

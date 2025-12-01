import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    splits = data_from_file(filename, count_beam_splits)
    print(f"Number of times the beam will be split: {splits}")

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

def count_beam_splits(file):
    grid = []
    splits = 0
    beam_splits = set()

    for y, line in enumerate(file):
        if 'S' in line:
            beam_splits.add((line.index('S'), y))
        #grid.append([c for c in line.strip()])
        grid.append(line.strip())

    assert len(beam_splits) == 1

    y = 0
    while y < len(grid) - 1:
        beams = beam_splits.copy()
        next_y = y + 1
        for beam in beams:
            if grid[next_y][beam[0]] == '^':
                # No line begins or ends with '^', so we don't bother checking
                # the value of beam[0] ± 1
                beam_splits.add((beam[0] + 1, next_y))
                beam_splits.add((beam[0] - 1, next_y))
                splits += 1
            else:
                beam_splits.add((beam[0], next_y))

            beam_splits.remove(beam)

        y += 1

    return splits

def debug_grid(grid):
    for line in grid:
        print(''.join(line))

class TestInvalidIDs(unittest.TestCase):
    def test_invalid_ids(self):
        splits = data_from_file('example.txt', count_beam_splits)
        self.assertEqual(splits, 21)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

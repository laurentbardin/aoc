import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    # 82 988 107 181 too low
    # 47 857 642 990 160
    timelines = data_from_file(filename, count_timelines)
    print(f"Number of possible timelines: {timelines}")

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

def count_timelines(file):
    grid = []
    beam_splits = set()
    beam_start = None

    for y, line in enumerate(file):
        if 'S' in line:
            beam_start = (line.index('S'), y)
        #grid.append([c for c in line.strip()])
        grid.append(line.strip())

    assert beam_start is not None

    beam_splits.add(beam_start)

    timeline_grid = [[0 for char in line] for line in grid]
    timeline_grid[beam_start[1]][beam_start[0]] = 1

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
                left = beam[0] - 1
                right = beam[0] + 1
                timeline_grid[next_y][left] += timeline_grid[y][beam[0]]
                timeline_grid[next_y][right] += timeline_grid[y][beam[0]]
            else:
                beam_splits.add((beam[0], next_y))
                timeline_grid[next_y][beam[0]] += timeline_grid[y][beam[0]]

            beam_splits.remove(beam)

        y += 1

    return sum(timeline_grid[-1])

class TestBeamTimelines(unittest.TestCase):
    def test_beam_timelines(self):
        timelines = data_from_file('example.txt', count_timelines)
        self.assertEqual(timelines, 40)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

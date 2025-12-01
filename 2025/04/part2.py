import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    total_rolls = data_from_file(filename, count_removable_rolls)
    print(f"Total umber of removable rolls of paper: {total_rolls}")

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

def count_removable_rolls(file):
    grid = []
    for line in file:
        grid.append([c for c in line.strip()])

    total = 0
    done = False
    max_h = len(grid) - 1
    max_w = len(grid[0]) - 1
    while not done:
        count = 0
        for y, line in enumerate(grid):
            for x, cell in enumerate(line):
                if grid[y][x] != '@':
                    continue

                adjacent_rolls = count_adjacent_rolls(x, y, grid, max_w, max_h)
                if adjacent_rolls < 4:
                    count += 1
                    grid[y][x] = '.'

        total += count
        done = count == 0

    return total

def count_adjacent_rolls(x, y, grid, max_width, max_height):
    count = 0
    for i in [y-1, y, y+1]:
        if i < 0 or i > max_height:
            continue
        for j in [x-1, x, x+1]:
            if j < 0 or j > max_width:
                continue
            if i == y and j == x:
                continue
            if grid[i][j] == '@':
                count += 1

    return count

def debug_grid(grid):
    for line in grid:
        print(''.join(line))

class TestInvalidIDs(unittest.TestCase):
    def test_invalid_ids(self):
        free_rolls = data_from_file('example.txt', count_removable_rolls)
        self.assertEqual(free_rolls, 43)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

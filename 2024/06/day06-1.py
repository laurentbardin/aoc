import re
import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    total = data_from_file(filename, analyze_grid)
    print(f"Visited positions: {total}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def analyze_grid(file):
    grid = []
    guard_position = None
    guard = re.compile(r"([<>v^])")

    for (line, data) in enumerate(file):
        data = data.strip()
        if guard_position is None:
            match = re.search(guard, data)
            if match is not None:
                guard_position = [match.start(), line]
        grid.append(data)

    assert guard_position is not None

    return guard_walk(guard_position, grid)

def guard_walk(position, grid):
    guard = grid[position[1]][position[0]]
    visited = set([tuple(position)])
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1

    while not guard_is_done(guard, position, max_x, max_y):
        if guard == '^':
            walk_north(position, grid, visited)
            if position[1] != 0:
                guard = '>'
        elif guard == '>':
            walk_east(position, grid, visited, max_x)
            if position[0] != max_x:
                guard = 'v'
        elif guard == 'v':
            walk_south(position, grid, visited, max_y)
            if position[1] != max_y:
                guard = '<'
        elif guard == '<':
            walk_west(position, grid, visited)
            if position[0] != 0:
                guard = '^'

    return len(visited)

def visit(position, visited):
    if position not in visited:
        visited.add(position)

def walk_north(position, grid, visited):
    while (position[1] > 0 and grid[position[1]-1][position[0]] != '#'):
        position[1] -= 1
        visit(tuple(position), visited)

def walk_east(position, grid, visited, max_x):
    while (position[0] < max_x and grid[position[1]][position[0]+1] != '#'):
        position[0] += 1
        visit(tuple(position), visited)

def walk_south(position, grid, visited, max_y):
    while (position[1] < max_y and grid[position[1]+1][position[0]] != '#'):
        position[1] += 1
        visit(tuple(position), visited)

def walk_west(position, grid, visited):
    while (position[0] > 0 and grid[position[1]][position[0]-1] != '#'):
        position[0] -= 1
        visit(tuple(position), visited)

def guard_is_done(guard, position, max_x, max_y):
    return guard == '^' and position[1] == 0 \
        or guard == '>' and position[0] == max_x \
        or guard == '<' and position[0] == 0 \
        or guard == 'v' and position[1] == max_y

def print_visited_path(grid, visited):
    """ Debug helper """
    visited_grid = []
    for (y, data) in enumerate(grid):
        positions = ''
        for (x, char) in enumerate(data):
            if (x, y) in visited:
                positions += 'X'
            else:
                positions += char
        visited_grid.append(positions)

    for line in visited_grid:
        print(line)

def data_from_file(filename, cb):
    try:
        with open(filename, 'r') as file:
            return cb(file)

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

class TestPuzzle(unittest.TestCase):
    visited = 0

    @classmethod
    def setUpClass(cls):
        cls.visited = data_from_file('example.txt', analyze_grid)

    def test_pages(self):
        self.assertEqual(self.visited, 41)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

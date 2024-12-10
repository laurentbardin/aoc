import re

import unittest

class Grid:
    """ Initialize the grid from the content of filename """
    def __init__(self, filename):
        self.grid = []

        try:
            with open(filename, 'r') as file:
                for (_, line) in enumerate(file):
                    """ Use an array of chars to easily add obstacles later """
                    line = line.strip()
                    places = [c for c in line]
                    self.grid.append(places)
        except OSError as e:
            print(f"Error reading '{filename}': {e.strerror}")
            raise e

        self.height = len(self.grid)
        self.width = len(self.grid[0])

        self.guard = ''
        self.guard_position = None
        self.find_guard()

        """ Build the list of obstacles on each line """
        self.obstacles = dict()
        self.find_obstacles()

    def print_grid(self, with_path=False):
        for (y, line) in enumerate(self.grid):
            for (x, char) in enumerate(line):
                if with_path and (x, y) in self.visited_places:
                    print('X', end='')
                else:
                    print(char, end='')
            print()

    def find_guard(self):
        guard = re.compile(r"([<>v^])")

        for (y, line) in enumerate(self.grid):
            match = re.search(guard, ''.join(line))
            if match is not None:
                self.guard = match.group(0)
                self.guard_position = (match.start(), y)
                break

        assert(self.guard_position is not None)

    def find_obstacles(self):
        for (y, line) in enumerate(self.grid):
            if y not in self.obstacles:
                self.obstacles[y] = []
            self.obstacles[y] = [i for i, c in enumerate(line) if c == '#']

    """
    First, we gather all the places the guard should visit. Then we place an
    obstactle on each of them and see if that triggers a loop in its patrol
    route. To do so, we keep a trace of all the places where he had to turn
    right. If he ever goes through one of them in the same direction, we have a
    loop.
    """
    def find_possible_loops(self):
        possible_loops = 0

        self.walk_guard()
        visited_places = self.visited_places.copy()
        for (x, y) in visited_places:
            self.find_guard() # Reset guard position
            if self.guard_position == (x, y):
                # Don't place an object on the guard
                continue
            self.set_object_at(x, y)
            try:
                self.walk_guard(detect_loop=True)
            except BaseException:
                possible_loops += 1

            self.unset_object_at(x, y)

        return possible_loops

    def walk_guard(self, detect_loop=False):
        self.visited_places = set([self.guard_position])
        self.turning_points = set()

        while not self.guard_is_done():
            match self.guard:
                case '^':
                    self.guard_position = self.walk_north()
                    if self.guard_position[1] > 0:
                        if detect_loop:
                            self.check_loop()
                        self.guard = '>'
                case '>':
                    self.guard_position = self.walk_east()
                    if self.guard_position[0] < self.width - 1:
                        if detect_loop:
                            self.check_loop()
                        self.guard = 'v'
                case 'v':
                    self.guard_position = self.walk_south()
                    if self.guard_position[1] < self.height - 1:
                        if detect_loop:
                            self.check_loop()
                        self.guard = '<'
                case '<':
                    self.guard_position = self.walk_west()
                    if self.guard_position[0] > 0:
                        if detect_loop:
                            self.check_loop()
                        self.guard = '^'

        return len(self.visited_places)

    def check_loop(self):
        if (self.guard_position, self.guard) in self.turning_points:
            raise BaseException
        else:
            self.turning_points.add((self.guard_position, self.guard))

    def walk_north(self):
        (x, y) = self.guard_position
        while (y > 0 and x not in self.obstacles[y-1]):
            y -= 1
            self.visited_places.add((x, y))

        return (x, y)

    def walk_east(self):
        (x, y) = self.guard_position
        while (x < self.width - 1 and x+1 not in self.obstacles[y]):
            x += 1
            self.visited_places.add((x, y))

        return (x, y)

    def walk_south(self):
        (x, y) = self.guard_position
        while (y < self.height - 1 and x not in self.obstacles[y+1]):
            y += 1
            self.visited_places.add((x, y))

        return (x, y)

    def walk_west(self):
        (x, y) = self.guard_position
        while (x > 0 and x-1 not in self.obstacles[y]):
            x -= 1
            self.visited_places.add((x, y))

        return (x, y)

    def guard_is_done(self):
        return self.guard == '^' and self.guard_position[1] == 0 \
            or self.guard == '>' and self.guard_position[0] == self.height - 1 \
            or self.guard == '<' and self.guard_position[0] == 0 \
            or self.guard == 'v' and self.guard_position[1] == self.width - 1

    def object_at(self, x, y):
        assert(0 <= x < self.width and 0 <= y < self.height)
        return self.grid[y][x]

    def set_object_at(self, x, y):
        assert(0 <= x < self.width and 0 <= y < self.height)
        self.grid[y][x] = '#'
        """ Reset the obstacles """
        self.find_obstacles()

    def unset_object_at(self, x, y):
        assert(0 <= x < self.width and 0 <= y < self.height)
        self.grid[y][x] = '.'
        """ Reset the obstacles """
        self.find_obstacles()

class GridTest(unittest.TestCase):
    grid = None

    @classmethod
    def setUpClass(cls):
        cls.grid = Grid('example.txt')

    def test_guard_walk(self):
        self.grid.walk_guard()
        self.assertEqual(len(self.grid.visited_places), 41)

class GridLoopTest(unittest.TestCase):
    grid = None

    @classmethod
    def setUpClass(cls):
        cls.grid = Grid('example.txt')

    def test_loop_detector(self):
        possible_loops = self.grid.find_possible_loops()
        self.assertEqual(possible_loops, 6)

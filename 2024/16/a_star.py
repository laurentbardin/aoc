import heapq

def solve(grid, start, dest, direction='>'):
    available = []
    available_dict = {}
    visited = set()

    start = Node(start)
    goal = Node(dest)

    start.direction = direction
    start.g = 0
    start.h = start.manhattan(goal)
    start.f = start.g + start.h

    heapq.heappush(available, (start.f, (start.x, start.y)))
    available_dict[(start.x, start.y)] = start

    path = None
    while len(available) > 0:
        _, current_position = heapq.heappop(available)
        current = available_dict[current_position]
        #print(f"Now on {current}")

        #print_grid(grid, reconstruct_path(current))
        #input("")

        if current == goal:
            #path = reconstruct_path(current)
            #print_grid(grid, path)
            return current.g

        visited.add(current_position)

        for neighbour_position in find_neighbours(grid, current):
            if neighbour_position in visited:
                continue

            tentative_g = current.g + current.cost(neighbour_position)

            if neighbour_position not in available_dict:
                neighbour = Node(neighbour_position)
                neighbour.direction = update_direction(current, neighbour_position)
                neighbour.parent = current
                neighbour.g = tentative_g
                neighbour.h = neighbour.manhattan(goal)
                neighbour.f = neighbour.g + neighbour.h

                #print(f"Making {neighbour} available: ", end='')
                heapq.heappush(available, (neighbour.f, neighbour_position))
                available_dict[neighbour_position] = neighbour
            elif tentative_g < available_dict[neighbour_position].g:
                neighbour = available_dict[neighbour_position]
                neighbour.direction = update_direction(current, neighbour_position)
                neighbour.parent = current
                neighbour.g = tentative_g
                neighbour.h = neighbour.manhattan(goal)
                neighbour.f = neighbour.g + neighbour.h
                #print(f"Found a better path to {neighbour_position}: ", end='')

            #print(f"g={neighbour.g} h={neighbour.h} dir={neighbour.direction}")

    assert path is None
    print("No path found!")

    return None

def print_grid(grid, path):
    for (y, line) in enumerate(grid):
        for (x, c) in enumerate(line):
            if (x, y) in path:
                print(path[(x, y)].direction, end='')
            else:
                print(c, end='')
        print()

def find_neighbours(grid, node):
    candidates = []

    match node.direction:
        case '^':
            candidates = [(node.x - 1, node.y), (node.x, node.y - 1), (node.x + 1, node.y)]
        case '>':
            candidates = [(node.x, node.y - 1), (node.x + 1, node.y), (node.x, node.y + 1)]
        case 'v':
            candidates = [(node.x + 1, node.y), (node.x, node.y + 1), (node.x - 1, node.y)]
        case '<':
            candidates = [(node.x, node.y + 1), (node.x - 1, node.y), (node.x, node.y - 1)]

    return [c for c in candidates if not is_wall(grid, c)]

def is_in_grid(grid, x, y):
    return 1 <= x < len(grid[0]) and 1 <= y < len(grid)

def is_wall(grid, position):
    x, y = position
    return grid[y][x] == '#'

def update_direction(orig, to):
    to_x, to_y = to
    # Same column
    if orig.x == to_x:
        if orig.y > to_y:
            direction = '^'
        else:
            direction = 'v'
    # Same line
    elif orig.y == to_y:
        if orig.x > to_x:
            direction = '<'
        else:
            direction = '>'

    return direction

def reconstruct_path(current):
    path = dict()

    while current is not None:
        path[(current.x, current.y)] = current
        current = current.parent

    return path

class Node(object):
    def __init__(self, position):
        self.x, self.y = position

        self.parent = None

        self.g = float('inf')
        self.h = 0
        self.f = 0

        # The direction when entering the node
        self.direction = '*'

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return self.f > other.f
    def __lt__(self, other):
        return self.f < other.f
    def __ge__(self, other):
        return self.f >= other.f
    def __le__(self, other):
        return self.f <= other.f

    def manhattan(self, dest):
        """
        Calculate the estimated cost of moving from self to dest (usually the
        goal node). If the direction is provided, take that into account.
        """
        distance = 0

        diff_x = self.x - dest.x
        diff_y = self.y - dest.y
        if self.direction is not None:
            if diff_x == 0:
                # We're on the same column
                if self.direction in '<>':
                    distance += 1000
                elif self.direction == 'v':
                    # We'll never be above the goal node, so we're not testing for it.
                    distance += 2000
            elif diff_y == 0:
                # We're on the same line
                if self.direction in '^v':
                    distance += 1000
                elif self.direction == '<':
                    # We'll never be right of the goal node, so we're not testing for it.
                    distance += 2000
            else:
                # We're to the left of and below the goal node
                if self.direction in '^>':
                    distance += 1000
                else:
                    # We have to turn twice
                    distance += 2000

        return distance + abs(diff_x) + abs(diff_y)

    def cost(self, position):
        """
        Calculate the cost (g) of moving FROM this node TO position, taking the
        current direction into account.
        """
        cost = 1

        nx, ny = position

        if self.x == nx and self.direction in '<>' or \
           self.y == ny and self.direction in '^v':
            cost += 1000

        return cost

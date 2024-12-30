import heapq

"""
Find the best path from start to dest on grid. The direction influences both
the cost (g) of a node and the estimation (h) for reaching goal from the
current position.
"""
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

    heapq.heappush(available, (start.f, start.position))
    available_dict[start.position] = start

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

    x, y = node.position
    match node.direction:
        case '^':
            candidates = [(x - 1, y), (x, y - 1), (x + 1, y)]
        case '>':
            candidates = [(x, y - 1), (x + 1, y), (x, y + 1)]
        case 'v':
            candidates = [(x + 1, y), (x, y + 1), (x - 1, y)]
        case '<':
            candidates = [(x, y + 1), (x - 1, y), (x, y - 1)]

    return [c for c in candidates if not is_wall(grid, c)]

def is_wall(grid, position):
    x, y = position
    return grid[y][x] == '#'

def update_direction(orig, to):
    x, y = orig.position
    to_x, to_y = to
    # Same column
    if x == to_x:
        if y > to_y:
            direction = '^'
        else:
            direction = 'v'
    # Same line
    elif y == to_y:
        if x > to_x:
            direction = '<'
        else:
            direction = '>'

    return direction

def reconstruct_path(current):
    path = dict()

    while current is not None:
        path[current.position] = current
        current = current.parent

    return path

class Node(object):
    def __init__(self, position):
        self.position = position

        self.parent = None

        self.g = float('inf')
        self.h = 0
        self.f = 0

        # The direction when entering the node
        self.direction = '*'

    def __str__(self):
        return f"{self.position}"

    def __eq__(self, other):
        x, y = self.position
        ox, oy = other.position
        return x == ox and y == oy
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

        x, y = self.position
        dest_x, dest_y = dest.position
        dx = x - dest_x
        dy = y - dest_y
        if self.direction is not None:
            if dx == 0:
                # We're on the same column
                if self.direction in '<>':
                    distance += 1000
                elif self.direction == 'v':
                    # We'll never be above the goal node, so we're not testing for it.
                    distance += 2000
            elif dy == 0:
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

        return distance + abs(dx) + abs(dy)

    def cost(self, other):
        """
        Calculate the cost (g) of moving FROM this node TO position, taking the
        current direction into account.
        """
        cost = 1

        x, y = self.position
        nx, ny = other

        if x == nx and self.direction in '<>' or \
           y == ny and self.direction in '^v':
            cost += 1000

        return cost

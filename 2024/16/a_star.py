import heapq

from node import Node

"""
Find the best path from start to dest on grid. The direction influences both
the cost (g) of a node and the estimation (h) for reaching goal from the
current position.
"""
def solve(grid, start, dest, *, base_g=0, max_score=float('inf'), direction='>'):
    available = []
    available_dict = {}
    visited = set()

    start = Node(start)
    goal = Node(dest)

    start.direction = direction
    start.g = base_g
    start.h = start.manhattan(goal)
    start.f = start.g + start.h

    heapq.heappush(available, (start.f, start.position))
    available_dict[start.position] = start

    path = None
    while len(available) > 0:
        _, current_position = heapq.heappop(available)
        current = available_dict[current_position]
        #print(f"Now on {current}")

        #if base_g > 0:
        #    print_grid(grid, reconstruct_path(current), available)
        #    print(f"Currently on {current.position}: g={current.g}, h={current.h}")
        #    input("")

        if current == goal:
            #path = reconstruct_path(current)
            #print_grid(grid, path, available)
            return current.g, reconstruct_path(current)

        visited.add(current_position)
        if current.g > max_score:
            continue

        for neighbour_position in find_neighbours(grid, current):
            if neighbour_position in visited:
                continue

            tentative_g = current.g + current.cost(neighbour_position)

            if neighbour_position not in available_dict:
                neighbour = Node(neighbour_position)
                neighbour.direction = update_direction(current.position, neighbour_position)
                neighbour.parent = current
                neighbour.g = tentative_g
                neighbour.h = neighbour.manhattan(goal)
                neighbour.f = neighbour.g + neighbour.h

                #print(f"Making {neighbour} available: ", end='')
                heapq.heappush(available, (neighbour.f, neighbour_position))
                available_dict[neighbour_position] = neighbour
            elif tentative_g < available_dict[neighbour_position].g:
                neighbour = available_dict[neighbour_position]
                neighbour.direction = update_direction(current.position, neighbour_position)
                neighbour.parent = current
                neighbour.g = tentative_g
                neighbour.h = neighbour.manhattan(goal)
                neighbour.f = neighbour.g + neighbour.h
                #print(f"Found a better path to {neighbour_position}: ", end='')


            #print(f"g={neighbour.g} h={neighbour.h} dir={neighbour.direction}")

    assert path is None
    #print("No path found!")

    # No path found
    return float('inf'), None

"""
Find all the possible best paths from start to dest on grid. The first path
found should be the best one (provided g is correcly calculated and h not
overestimated). We then walk that best path and check any unexplored neighbour
to see if it leads do dest without going over the score of the best path.
Each new path found is then explored on its own until all possible alternate
routes have been explored.
"""
def solve_multiple(grid, start, dest, direction='>'):
    best_score, best_path = solve(grid, start, dest, direction=direction)

    paths = [best_path]
    nodes = set(best_path.keys())
    available_paths = [best_path]
    while len(available_paths) > 0:
        path = available_paths.pop()

        for position in path.keys():
            if position == dest:
                continue

            neighbours = find_neighbours(grid, path[position])
            for neighbour_position in neighbours:
                if neighbour_position in path.keys():
                    continue

                node = path[position]
                base_g = node.g + node.cost(neighbour_position)
                direction = update_direction(node.position, neighbour_position)
                score, new_path = solve(grid, neighbour_position, dest, base_g=base_g, direction=direction, max_score=best_score)
                if new_path is not None:
                    new_nodes = set(new_path.keys()) - nodes
                    new_path = {node: new_path[node] for node in new_path.keys() if node in new_nodes}
                    nodes |= new_nodes
                    available_paths.append(new_path)
                    paths.append(new_path)

    return best_score, paths

def print_grid(grid, path, available):
    available_pos = [p for _, p in available]
    for (y, line) in enumerate(grid):
        for (x, c) in enumerate(line):
            if (x, y) in path:
                if isinstance(path, set):
                    print('O', end='')
                else:
                    print(path[(x, y)].direction, end='')
            elif (x, y) in available_pos:
                print('?', end='')
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

def update_direction(position, to):
    x, y = position
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

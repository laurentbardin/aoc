import heapq

from node import Node

"""
Find the best path from start to dest on grid. Simplified version from day 16,
as the direction is now irrelevant.
"""
def solve(grid, start, dest, *, base_g=0, max_score=float('inf')):
    available = []
    available_dict = {}
    visited = set()

    start = Node(start)
    goal = Node(dest)

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
                neighbour.parent = current
                neighbour.g = tentative_g
                neighbour.h = neighbour.manhattan(goal)
                neighbour.f = neighbour.g + neighbour.h

                #print(f"Making {neighbour} available: ", end='')
                heapq.heappush(available, (neighbour.f, neighbour_position))
                available_dict[neighbour_position] = neighbour
            elif tentative_g < available_dict[neighbour_position].g:
                neighbour = available_dict[neighbour_position]
                neighbour.parent = current
                neighbour.g = tentative_g
                neighbour.h = neighbour.manhattan(goal)
                neighbour.f = neighbour.g + neighbour.h
                #print(f"Found a better path to {neighbour_position}: ", end='')


            #print(f"g={neighbour.g} h={neighbour.h}")

    assert path is None
    print("No path found!")

    # No path found
    return float('inf'), None

def print_grid(grid, path, available):
    available_pos = [p for _, p in available]
    for (y, line) in enumerate(grid):
        for (x, c) in enumerate(line):
            if (x, y) in path:
                if isinstance(path, set):
                    print('O', end='')
                else:
                    print('.', end='')
            elif (x, y) in available_pos:
                print('?', end='')
            else:
                print(c, end='')
        print()

def find_neighbours(grid, node):
    candidates = []

    x, y = node.position
    candidates = [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]

    return [c for c in candidates if is_inbound(grid, c) and not is_wall(grid, c)]

def is_inbound(grid, position):
    x, y = position
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

def is_wall(grid, position):
    x, y = position
    return grid[y][x] == '#'

def reconstruct_path(current):
    path = dict()

    while current is not None:
        path[current.position] = current
        current = current.parent

    return path

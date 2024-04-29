import sys

def main():
    pipe_map = data_from_file('example-1.txt')

    loop_length = count_steps(pipe_map)

def data_from_file(filename):
    pipe_map = []

    with open(filename, 'r') as file:
        for _, data in enumerate(file):
            pipe_map.append(data.splitlines()[0])

    return pipe_map

def count_steps(pipe_map):
    (x, y) = find_starting_position(pipe_map)
    if x is None and y is None:
        print('No starting position found, aborting')
        sys.exit(0)

    steps = 0

    current_pipe = (x, y)
    next_pipe = find_first_pipe(pipe_map, x, y)

    while next_pipe[0] != x and next_pipe[1] != y:
        steps += 1
        next_pipe = find_next_pipe(pipe_map, (x, y), next_pipe)

    print((x, y))

def find_first_pipe(pipe_map, x, y):
    """
    Look left and right to find the first pipe in the loop (not counting
    the starting pipe, given by the x and y coordinates). Given that there are
    only two pipes connected to the starting position, if neither is on the left
    or right we'll return the up one.
    """
    if pipe_map[y][x-1] in ['-', 'L', 'F']:
        return (x-1, y)
    elif pipe_map[y][x+1] in ['-', '7', 'J']:
        return (x+1, y)
    else:
        return (x, y+1)

def find_next_pipe(pipe_map, form_pipe, pipe):
    """
    Find the next pipe
    pass

def find_starting_position(pipe_map):
    for line, data in enumerate(pipe_map):
        try:
            return (data.index('S'), line)
        except ValueError:
            continue

    return (None, None)

if __name__ == '__main__':
    main()

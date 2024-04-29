import sys
import unittest
from dataclasses import dataclass

def main():
    pipe_map = data_from_file('data.txt')

    loop_length = count_steps(pipe_map)
    print(f'Loop length: {loop_length} => farthest point at {loop_length / 2}')

def data_from_file(filename):
    pipe_map = []

    with open(filename, 'r') as file:
        for _, data in enumerate(file):
            pipe_map.append(data.splitlines()[0])

    return pipe_map

def count_steps(pipe_map):
    start_pipe = find_starting_position(pipe_map)
    if start_pipe.x is None and start_pipe.y is None:
        print('No starting position found, aborting')
        sys.exit(0)

    # Count the starting pipe
    steps = 1

    current_pipe = start_pipe
    next_pipe = find_first_pipe(pipe_map, start_pipe)

    while next_pipe - start_pipe != (0, 0):
        steps += 1
        (current_pipe, next_pipe) = (next_pipe, find_next_pipe(pipe_map, current_pipe, next_pipe))


    return steps

def find_first_pipe(pipe_map, start_pipe):
    """
    Look left and right to find the first pipe in the loop (not counting
    the starting pipe, given by the x and y coordinates). Given that there are
    only two pipes connected to the starting position, if neither is on the left
    or right we'll return the up one.
    """
    if pipe_map[start_pipe.y][start_pipe.x-1] in ['-', 'L', 'F']:
        return Pipe(start_pipe.x-1, start_pipe.y)
    elif pipe_map[start_pipe.y][start_pipe.x+1] in ['-', '7', 'J']:
        return Pipe(start_pipe.x+1, start_pipe.y)
    else:
        return Pipe(start_pipe.x, start_pipe.y+1)

def find_next_pipe(pipe_map, from_pipe, pipe):
    """
    Find the next pipe considering we are currently at pipe, coming from from_pipe
    """
    symbol = pipe_map[pipe.y][pipe.x]
    new_pipe = None

    match pipe - from_pipe:
        case (0, 1): # coming from above
            match symbol:
                case '|':
                    new_pipe = Pipe(pipe.x, pipe.y + 1)
                case 'J':
                    new_pipe = Pipe(pipe.x - 1, pipe.y)
                case 'L':
                    new_pipe = Pipe(pipe.x + 1, pipe.y)
        case (0, -1): # coming from below
            match symbol:
                case '|':
                    new_pipe = Pipe(pipe.x, pipe.y - 1)
                case 'F':
                    new_pipe = Pipe(pipe.x + 1, pipe.y)
                case '7':
                    new_pipe = Pipe(pipe.x - 1, pipe.y)
        case (1, 0): # coming from the left
            match symbol:
                case '-':
                    new_pipe = Pipe(pipe.x + 1, pipe.y)
                case 'J':
                    new_pipe = Pipe(pipe.x, pipe.y - 1)
                case '7':
                    new_pipe = Pipe(pipe.x, pipe.y + 1)
        case (-1, 0): # coming from the right
            match symbol:
                case '-':
                    new_pipe = Pipe(pipe.x - 1, pipe.y)
                case 'F':
                    new_pipe = Pipe(pipe.x, pipe.y + 1)
                case 'L':
                    new_pipe = Pipe(pipe.x, pipe.y - 1)

    assert(new_pipe is not None)
    assert(new_pipe.x >= 0)
    assert(new_pipe.y >= 0)

    return new_pipe

def find_starting_position(pipe_map):
    for line, data in enumerate(pipe_map):
        try:
            return Pipe(data.index('S'), line)
        except ValueError:
            continue

    return Pipe(None, None)

@dataclass
class Pipe:
    x: int
    y: int

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __sub__(self, other):
        return (self.x - other.x, self.y - other.y)

class TestPipe(unittest.TestCase):
    def test_pipe_calculations(self):
        first_pipe = Pipe(2, 2)
        second_pipe = Pipe(2, 3)
        self.assertTupleEqual(second_pipe - first_pipe, (0, 1))
        second_pipe = Pipe(2, 1)
        self.assertTupleEqual(second_pipe - first_pipe, (0, -1))
        second_pipe = Pipe(3, 2)
        self.assertTupleEqual(second_pipe - first_pipe, (1, 0))
        second_pipe = Pipe(1, 2)
        self.assertTupleEqual(second_pipe - first_pipe, (-1, 0))

if __name__ == '__main__':
    main()

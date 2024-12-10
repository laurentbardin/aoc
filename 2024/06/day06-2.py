import re
import sys
import unittest

from Grid import Grid

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    try:
        grid = Grid(filename)
    except OSError:
        sys.exit(1)

    possible_loops = grid.find_possible_loops()
    print(f"Number of possible loops: {possible_loops}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

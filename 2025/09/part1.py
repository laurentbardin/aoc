import sys
import unittest

from dataclasses import dataclass
from operator import itemgetter

@dataclass
class Tile:
    x: int
    y: int

    def area(self, other):
        width = abs(self.x - other.x) + 1
        height = abs(self.y - other.y) + 1
        return width * height

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    area = data_from_file(filename, find_largest_area)
    print(f"Largest area: {area}")

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

def find_largest_area(file):
    tiles = []

    for line in file:
        x, y = map(int, line.strip().split(','))
        tile = Tile(x, y)
        tiles.append((x, tile))

    tiles.sort(key=itemgetter(0))

    largest_area = 0
    for i, tile1 in enumerate(tiles):
        for tile2 in tiles[i+1:]:
            largest_area = max(largest_area, tile1[1].area(tile2[1]))

    return largest_area

class TestLargestArea(unittest.TestCase):
    def test_largest_area(self):
        area = data_from_file('example.txt', find_largest_area)
        self.assertEqual(area, 50)

    def test_area(self):
        t1 = Tile(2, 5)
        t2 = Tile(11, 1)
        self.assertEqual(t1.area(t2), 50)

        t1 = Tile(2, 5)
        t2 = Tile(2, 9)
        self.assertEqual(t1.area(t2), 5)

        t1 = Tile(9, 5)
        t2 = Tile(2, 5)
        self.assertEqual(t1.area(t2), 8)

        t1 = Tile(5, 6)
        t2 = Tile(5, 6)
        self.assertEqual(t1.area(t2), 1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

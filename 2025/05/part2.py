import sys
import unittest

from collections import namedtuple

Range = namedtuple('Range', ['min', 'max'])

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    fresh_ingredients = data_from_file(filename, count_fresh_ingredients)
    print(f"Fresh ingredients: {fresh_ingredients}")

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

def count_fresh_ingredients(file):
    fresh_ids = []
    fresh_ingredients = 0

    for rg in file:
        rg = rg.strip()

        if not rg:
            break

        low, high = map(int, rg.split('-'))
        fresh_ids.append(Range(low, high))

    fresh_ids = collapse_ranges(fresh_ids)
    for range in fresh_ids:
        fresh_ingredients += range.max - range.min + 1

    return fresh_ingredients

def collapse_ranges(ranges):
    collapsed = []
    ranges.sort()

    i = 0
    current = ranges[i]
    while i < len(ranges) - 1:
        next = ranges[i+1]

        if next.min <= current.max:
            current = Range(current.min, max(current.max, next.max))
        else:
            collapsed.append(current)
            current = next

        i += 1

    collapsed.append(current)

    return collapsed

class TestFreshIngredients(unittest.TestCase):
    def test_fresh_ingredients(self):
        fresh_ingredients = data_from_file('example.txt', count_fresh_ingredients)
        self.assertEqual(fresh_ingredients, 14)

    def test_range_collapse_with_overlap(self):
        ranges = [Range(7, 10), Range(3, 8)]
        collapsed = collapse_ranges(ranges)
        self.assertListEqual(collapsed, [Range(3, 10)])

    def test_range_collapse_without_overlap(self):
        ranges = [Range(10, 15), Range(3, 8)]
        collapsed = collapse_ranges(ranges)
        self.assertListEqual(collapsed, ranges)

    def test_range_collapse_with_total_overlap(self):
        ranges = [Range(7, 10), Range(3, 12)]
        collapsed = collapse_ranges(ranges)
        self.assertListEqual(collapsed, [Range(3, 12)])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

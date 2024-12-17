import sys
import unittest

from Garden import Garden

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    total_price = data_from_file(filename, analyze_garden)
    print(f"Total price to fence the regions: {total_price}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def analyze_garden(file):
    garden = Garden(file)
    garden.find_regions()

    return garden.price()

def data_from_file(filename, cb):
    try:
        with open(filename, 'r') as file:
            return cb(file)

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

class TestTopography(unittest.TestCase):

    def test_garden_1(self):
        price = data_from_file('example-1.txt', analyze_garden)
        self.assertEqual(price, 140)

    def test_garden_2(self):
        price = data_from_file('example-2.txt', analyze_garden)
        self.assertEqual(price, 772)

    def test_garden_3(self):
        price = data_from_file('example-3.txt', analyze_garden)
        self.assertEqual(price, 1930)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

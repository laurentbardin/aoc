import sys
import unittest

from Warehouse import Warehouse

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    gps_sum = data_from_file(filename, analyze_warehouse)
    print(f"Sum of all the boxes' GPS coordinates: {gps_sum}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def analyze_warehouse(file):
    positions = []
    movements = ''
    for (_, line) in enumerate(file):
        line = line.splitlines()[0]
        if line.find('#') == 0:
            positions.append(line)
        elif line != '':
            movements += line

    warehouse = Warehouse(positions)

    for direction in movements:
        warehouse.move_robot(direction)

    return warehouse.sum_gps_coordinates()

def data_from_file(filename, cb):
    try:
        with open(filename, 'r') as file:
            return cb(file)

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

class TestTopography(unittest.TestCase):

    def test_gps_coordinates_1(self):
        gps_sum = data_from_file('example-1.txt', analyze_warehouse)
        self.assertEqual(gps_sum, 10092)

    def test_gps_coordinates_2(self):
        gps_sum = data_from_file('example-2.txt', analyze_warehouse)
        self.assertEqual(gps_sum, 2028)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

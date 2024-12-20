import sys
import unittest

from Area import Area, Robot

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    area = Area()
    safety_factor = data_from_file(filename, analyze_robots, area)
    print(f"Safety factor: {safety_factor}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def analyze_robots(file, area):
    for (_, line) in enumerate(file):
        (p, v) = line.splitlines()[0].split()
        p = tuple([int(c) for c in p.split('=')[1].split(',')])
        v = tuple([int(s) for s in v.split('=')[1].split(',')])

        area.add_robot(Robot(p, v))

    area.simulate_robots()

    return area.get_safety_factor()

def data_from_file(filename, cb, area):
    try:
        with open(filename, 'r') as file:
            return cb(file, area)

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

class TestTopography(unittest.TestCase):

    def test_safety_factor(self):
        area = Area(11, 7)
        safety_factor = data_from_file('example.txt', analyze_robots, area)
        self.assertEqual(safety_factor, 12)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

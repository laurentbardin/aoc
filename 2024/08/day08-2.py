import sys
import unittest

from Map import Map

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    antinodes = Map(filename).count_antinodes_with_resonance()
    print(f"Number of distinct antinodes: {antinodes}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

class TestCalibration(unittest.TestCase):
    Map = None

    @classmethod
    def setUpClass(cls):
        cls.Map = Map('example.txt')

    def test_calibrations(self):
        self.assertEqual(self.Map.count_antinodes_with_resonance(), 34)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

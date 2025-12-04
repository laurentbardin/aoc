import sys
import unittest
import re

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    result = sum(get_invalid_ids(filename))
    print(f"Sum of invalid IDs: {result}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def get_invalid_ids(filename):
    invalid_ids = []
    pattern = re.compile(r'^(\d+)\1$')
    try:
        with open(filename, 'r') as file:
            for r in file.readline().strip().split(','):
                low, high = map(int, r.split('-'))
                for n in map(str, range(low, high + 1)):
                    if len(n) % 2 == 0 and pattern.match(n):
                        invalid_ids.append(int(n))

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

    return invalid_ids

class TestInvalidIDs(unittest.TestCase):
    def test_invalid_ids(self):
        result = sum(get_invalid_ids('example.txt'))
        self.assertEqual(result, 1227775554)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

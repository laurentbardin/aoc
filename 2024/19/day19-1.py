import re
import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    possible_designs = data_from_file(filename, analyze_towels)
    print(f"Number of possible designs: {possible_designs}")

def analyze_towels(file):
    regex = None
    designs = []
    for _, s in enumerate(file):
        s = s.splitlines()[0]

        if ',' in s:
            stripes = s.split(', ')
            regex = "^(?:" + '|'.join(stripes) + ")+$"
        elif s != '':
            designs.append(s)

    assert regex is not None
    regex = re.compile(regex)

    # Fancy counting for loop
    valid_designs = [0 if regex.search(d) is None else 1 for d in designs]

    return sum(valid_designs)

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

class TestDistances(unittest.TestCase):
    def test_towels(self):
        designs = data_from_file('example.txt', analyze_towels)
        self.assertEqual(designs, 6)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

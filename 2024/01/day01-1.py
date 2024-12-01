import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    pairs = [pair for pair in data_from_file(filename)]
    print(f"Sum of the distances: {sum_distances(pairs)}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def data_from_file(filename):
    list_a = []
    list_b = []

    try:
        with open(filename, 'r') as file:
            for (line, data) in enumerate(file):
                (a, b) = data.splitlines()[0].split()
                list_a.append(int(a))
                list_b.append(int(b))

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

    # Sort the lists so that the smaller numbers in each one are associated with
    # each other
    list_a.sort()
    list_b.sort()
    return zip(list_a, list_b)

def sum_distances(pairs):
    total = 0
    for p in pairs:
        total += abs(p[0] - p[1])

    return total

class TestDistances(unittest.TestCase):
    pairs = None

    @classmethod
    def setUpClass(cls):
        data = data_from_file('example.txt')
        cls.pairs = [pair for pair in data]

    def test_pairs(self):
        self.assertEqual(self.pairs, [(1, 3), (2, 3), (3, 3), (3, 4), (3, 5), (4, 9)])

    def test_sum(self):
        self.assertEqual(sum_distances(self.pairs), 11)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

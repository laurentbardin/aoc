import sys
import unittest

from Trie import Trie

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    arrangements = data_from_file(filename, analyze_towels)
    print(f"Total number of possible arrangements: {arrangements}")

def analyze_towels(file):
    towels = []
    designs = []
    for _, s in enumerate(file):
        s = s.splitlines()[0]

        if ',' in s:
            towels = s.split(', ')
        elif s != '':
            designs.append(s)

    tree = Trie('bgruw')
    for t in towels:
        tree.insert(t[::-1])

    arrangements = []
    for d in designs:
        # count[i] == number of ways to make design up to d[i]
        count = [0] * len(d)

        for i in range(len(d)):
            node = tree.root
            for j in range(i, -1, -1):
                color = d[j]

                if node.children[color] is None:
                    break

                node = node.children[color]

                if node.is_word:
                    if j > 0:
                        count[i] += count[j - 1]
                    else:
                        count[i] += 1

        arrangements.append(count[-1])

    return sum(arrangements)

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
    def test_arrangements(self):
        arrangements = data_from_file('example.txt', analyze_towels)
        self.assertEqual(arrangements, 16)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

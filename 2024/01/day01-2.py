import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    (list_a, list_b) = data_from_file(filename)

    print(f"Similarity score: {similarity_score(list_a, list_b)}")

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

    return (list_a, list_b)

def similarity_score(list_a, list_b):
    similarity_score = 0
    for n in list_a:
        occurences = list_b.count(n)
        similarity_score += n * occurences

    return similarity_score

class TestDistances(unittest.TestCase):
    list_a = None
    list_b = None

    @classmethod
    def setUpClass(cls):
        (cls.list_a, cls.list_b) = data_from_file('example.txt')

    def test_similarity_score(self):
        self.assertEqual(similarity_score(self.list_a, self.list_b), 31)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

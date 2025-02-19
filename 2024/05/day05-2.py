import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    total = data_from_file(filename, analyze_pages)
    print(f"Sum of corrected pages: {total}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def analyze_pages(file):
    rules = []
    pages = []

    for (_, data) in enumerate(file):
        content = data.strip()
        if content == '':
            break
        rules.append([n for n in map(int, content.split('|'))])

    for (_, data) in enumerate(file):
        content = data.strip()
        pages.append([n for n in map(int, content.split(','))])

    return check_pages(rules, pages)

def check_pages(rules, pages):
    corrected_pages = []

    """
    For each list of pages to print, check it is in the correct order. If not,
    swap the infringing numbers and check the rules again, from the start.
    """
    for p in pages:
        correct = False
        corrections = 0
        while not correct:
            for r in rules:
                if r[0] in p and r[1] in p:
                    left = p.index(r[0])
                    right = p.index(r[1])
                    if left > right:
                        (p[left], p[right]) = (r[1], r[0])
                        corrections += 1
                        break
            else:
                correct = True
                if corrections > 0:
                    assert len(p) % 2 == 1
                    corrected_pages.append(p[len(p) // 2])
                    corrections = 0


    return sum(corrected_pages)

def data_from_file(filename, cb):
    try:
        with open(filename, 'r') as file:
            return cb(file)

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

class TestPuzzle(unittest.TestCase):
    pages = 0

    @classmethod
    def setUpClass(cls):
        cls.pages = data_from_file('example.txt', analyze_pages)

    def test_pages(self):
        self.assertEqual(self.pages, 123)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

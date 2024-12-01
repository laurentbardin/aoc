import re
import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    total = data_from_file(filename, analyze_memory)
    print(f"Total: {total}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def analyze_memory(file):
    products = []
    pattern = re.compile(r"mul\((\d+),(\d+)\)")

    for (_, data) in enumerate(file):
        for match in pattern.finditer(data):
            products.append(int(match.group(1)) * int(match.group(2)))

    return sum(products)

def data_from_file(filename, cb):
    try:
        with open(filename, 'r') as file:
            return cb(file)

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

class TestReports(unittest.TestCase):
    total = 0

    @classmethod
    def setUpClass(cls):
        cls.total = data_from_file('example-1.txt', analyze_memory)

    def test_reports(self):
        self.assertEqual(self.total, 161)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

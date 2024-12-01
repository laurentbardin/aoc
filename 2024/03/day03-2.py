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
    do = True
    pattern = re.compile(r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)")

    for (_, data) in enumerate(file):
        for match in pattern.finditer(data):
            if match.group(0) == 'do()':
                do = True
            elif match.group(0) == "don't()":
                do = False
            elif do:
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
        cls.total = data_from_file('example-2.txt', analyze_memory)

    def test_reports(self):
        self.assertEqual(self.total, 48)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

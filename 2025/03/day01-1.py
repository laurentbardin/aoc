import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    total = sum(data_from_file(filename, get_joltage_output))
    print(f"Total joltage output: {total}")

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

def get_joltage_output(file):
    batteries = []
    for bank in file:
        bank = bank.strip()
        best = 0
        start = 0
        end = len(bank)

        while start < end:
            i = int(bank[start])
            if i >= best // 10:
                for j in bank[start+1:]:
                    joltage = 10*i + int(j)
                    if joltage > best:
                        best = joltage

            start += 1

        batteries.append(best)

    return batteries

class TestInvalidIDs(unittest.TestCase):
    def test_invalid_ids(self):
        total = sum(data_from_file('example.txt', get_joltage_output))
        self.assertEqual(total, 357)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    safe_reports = data_from_file(filename, analyze_report)
    print(f"Number of safe reports: {safe_reports}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def analyze_report(file):
    safe_reports = 0

    for (line, data) in enumerate(file):
        for report in data.splitlines():
            if is_safe(report):
                safe_reports += 1

    return safe_reports

def is_safe(report):
    ascending, descending = False, False

    levels = list(map(int, report.split()))

    # Check the first two levels: if they're equal we can exit early, otherwise
    # we set our expectation about the list sort order (ascending or
    # descending)
    if levels[0] == levels[1]:
        return False
    elif levels[0] > levels[1]:
        descending = True
    else:
        ascending = True

    prev_level = levels[0]
    for next_level in levels[1:]:
        if next_level == prev_level:
            return False
        elif next_level > prev_level and descending:
            return False
        elif next_level < prev_level and ascending:
            return False
        elif abs(prev_level - next_level) > 3:
            return False
        else:
            prev_level = next_level

    return True

def data_from_file(filename, cb):
    try:
        with open(filename, 'r') as file:
            return cb(file)

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

class TestReports(unittest.TestCase):
    safe_reports = None

    @classmethod
    def setUpClass(cls):
        cls.safe_reports = data_from_file('example.txt', analyze_report)

    def test_reports(self):
        self.assertEqual(self.safe_reports, 2)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

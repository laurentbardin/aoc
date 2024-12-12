import sys
import unittest

from Map import Map

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    score = data_from_file(filename, analyze_map)
    print(f"Total trails score: {score}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def analyze_map(file):
    score = 0

    topography = Map(file)
    for (x, y) in topography.find_zeroes():
        #print(f"Looking at 0 @ ({x},{y})...")
        trails_end = set()
        #for candidate in topography.get_candidates(x, y):
        #    print(f"Candidate: ({candidate[0]},{candidate[1]})")
        for (next_x, next_y) in topography.walk_trail(x, y):
            if topography.slope_at(next_x, next_y) == 9:
                #print(f"Got result from ({next_x},{next_y})")
                trails_end.add((next_x, next_y))
                #print(f"Current tally: {trails_end}")

        score += len(trails_end)

    return score

def data_from_file(filename, cb):
    try:
        with open(filename, 'r') as file:
            return cb(file)

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

class TestTopography(unittest.TestCase):

    def test_trails(self):
        score = data_from_file('example.txt', analyze_map)
        self.assertEqual(score, 36)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

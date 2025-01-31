import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    total_stones = data_from_file(filename, analyze_stones)
    print(f"Final number of stones: {total_stones}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def analyze_stones(file):
    stones = list(map(int, file.readline().strip().split()))

    total = 0
    for (idx, stone) in enumerate(stones):
        total += 1
        """
        Running the same solution for part 1 is unpractical, as the number of
        iterations grows exponentially (or close to it) as you blink more
        times. We'll skip this for now and revisit it later by adding some form
        of cache, as we're bound to get some stones multiple times. That way,
        we'll be able to lookup the result of said stone after n iterations,
        and skip them altogether.

        TODO: Look up caching data structures, probably some form of Tree or another
        """
        total += blink_stone(stone, 75)

    return total

def blink_stone(stone, iterations):
    if iterations == 0:
        return 0

    added_stone = 0
    if stone == 0:
        added_stone += blink_stone(1, iterations - 1)
    elif len(str(stone)) % 2 == 0:
        s = str(stone)
        size = len(s) // 2
        added_stone = 1
        for new_stone in [s[:size], s[size:]]:
            added_stone += blink_stone(int(new_stone), iterations - 1)
    else:
        added_stone += blink_stone(stone * 2024, iterations - 1)

    return added_stone

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
        stones = data_from_file('example.txt', analyze_stones)
        self.assertEqual(stones, 55312)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

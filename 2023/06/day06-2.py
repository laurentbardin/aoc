def main():
    (time, distance) = data_from_file('data.txt')

    winnings = count_possible_winnings(time, distance)

    print(f'Total number of winning distances: {winnings}')

def data_from_file(filename):
    time = None
    distance = None

    with open(filename, 'r') as file:
        for (line, data) in enumerate(file):
            (kind, value) = data.splitlines()[0].split(':')
            value = int(''.join(value.split()))

            if kind == 'Time':
                time = value
            elif kind == 'Distance':
                distance = value

    return (time, distance)

def count_possible_winnings(race_duration, record):
    """
    Count the number of possible winning given a race duration and the distance
    to beat.
    """
    max_distance = 0
    winning_distances = 0

    # Distances grow from 0 up to a maximum. Once that maximum is reached, it's
    # only downhill from there.
    for distance in distance_traveled(race_duration):
        if distance <= record:
            continue
        elif distance <= max_distance:
            winning_distances = winning_distances * 2 - 1
            break
        elif distance == max_distance:
            winning_distances = winning_distances * 2
            break
        else:
            winning_distances += 1

    return winning_distances

def distance_traveled(race_duration):
    """
    Generate the distances traveled for a race running for race_duration
    milliseconds.
    """
    assert race_duration >= 0
    for hold_duration in range(0, race_duration + 1):
        yield hold_duration * (race_duration - hold_duration)

import unittest

class TestDistances(unittest.TestCase):

    def test_values(self):
        (time, distance) = data_from_file('example-1.txt')
        self.assertEqual(time, 71530)
        self.assertEqual(distance, 940200)

    def test_distance_traveled(self):
        self.assertEqual(count_possible_winnings(7, 9), 4)
        self.assertEqual(count_possible_winnings(15, 40), 8)
        self.assertEqual(count_possible_winnings(30, 200), 9)
        self.assertEqual(count_possible_winnings(30, 300), 0)

if __name__ == '__main__':
    main()

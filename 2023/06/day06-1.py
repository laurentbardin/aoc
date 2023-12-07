def main():
    values = data_from_file('data.txt')
    winning_distances = [
        len([distance for distance in distance_traveled(time) if distance > record])
        for (time, record) in values
    ]

    product = 1
    for n in winning_distances:
        product *= n

    print(f'{winning_distances}: {product}')

def data_from_file(filename):
    times = []
    distances = []

    with open(filename, 'r') as file:
        for (line, data) in enumerate(file):
            values = [int(v) for v in
                      data.splitlines()[0].split(':')[1].split()]

            if data.startswith('Time'):
                times = values
            elif data.startswith('Distance'):
                distances = values

    return zip(times, distances)

def distance_traveled(race_duration):
    """
    Generate the distances traveled for a race running for race_duration
    milliseconds.
    """
    assert(race_duration >= 0)
    for hold_duration in range(0, race_duration + 1):
        yield hold_duration * (race_duration - hold_duration)

import unittest

class TestDistances(unittest.TestCase):
    data = None

    @classmethod
    def setUpClass(cls):
        cls.data = data_from_file('example-1.txt')

    def test_distance_traveled(self):
        expected = {
            7: [0, 6, 10, 12, 12, 10, 6, 0],
            15: [0, 14, 26, 36, 44, 50, 54, 56, 56, 54, 50, 44, 36, 26, 14, 0],
            30: [0, 29, 56, 81, 104, 125, 144, 161, 176, 189, 200, 209, 216,
                 221, 224, 225, 224, 221, 216, 209, 200, 189, 176, 161, 144,
                 125, 104, 81, 56, 29, 0],
        }
        for (time, record) in self.data:
            distances = [d for d in distance_traveled(time)]
            self.assertEqual(distances, expected[time])

if __name__ == '__main__':
    main()

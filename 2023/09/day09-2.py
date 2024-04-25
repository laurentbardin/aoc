import unittest

def main():
    reports = data_from_file('data.txt')

    extrapolations = []
    for report in reports:
        extrapolations.append(get_extrapolation(report))

    print(f'Sum of all backward extrapolations: {sum(extrapolations)}')

def data_from_file(filename):
    #reports = []
    with open(filename, 'r') as file:
        for _, data in enumerate(file):
            #reports.append([int(n) for n in data.splitlines()[0].split()])
            yield [int(n) for n in data.splitlines()[0].split()]

def get_extrapolation(report):
    if not any(report):
        return 0

    difference = get_extrapolation(get_differences(report))

    return report[0] - difference

def get_differences(report):
    differences = [report[i + 1] - report[i] for i in range(len(report) - 1)]

    return differences

class TestIt(unittest.TestCase):
    def test_differences(self):
        self.assertListEqual(get_differences([0, 3, 6, 9, 12, 15]),
                             [3, 3, 3, 3, 3])
        self.assertListEqual(get_differences([3, 3, 3, 3, 3]),
                             [0, 0, 0, 0])

    def test_differences_with_negative_numbers(self):
        self.assertListEqual(get_differences([-2, -4, 6, 8, 10]),
                             [-2, 10, 2, 2])
        self.assertListEqual(get_differences([-3, -3, -3, -3, -3]),
                             [0, 0, 0, 0])

    def test_extrapolation(self):
        self.assertEqual(get_extrapolation([0, 3, 6, 9, 12, 15]), -3)
        self.assertEqual(get_extrapolation([1, 3, 6, 10, 15, 21]), 0)
        self.assertEqual(get_extrapolation([10, 13, 16, 21, 30, 45]), 5)

    def test_main(self):
        reports = data_from_file('example-1.txt')

        extrapolations = []
        for report in reports:
            extrapolations.append(get_extrapolation(report))

        self.assertEqual(sum(extrapolations), 2)

if __name__ == '__main__':
    main()

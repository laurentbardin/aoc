import unittest

from poker.Hand import Hand

hands = []

def main():
    data_from_file('data.txt')

    total_amount = get_total_winnings()

    print(f'Total amount: {total_amount}')

def get_total_winnings():
    total_amount = 0

    for (rank, hand) in enumerate(hands):
        total_amount += hand.bid * (rank + 1)

    return total_amount

def data_from_file(filename):
    with open(filename, 'r') as file:
        for (line, data) in enumerate(file):
            hands.append(Hand(*data.splitlines()[0].split(), True))

    hands.sort()

class TestResult(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data_from_file('example-1.txt')

    def test_amount(self):
        self.assertEqual(get_total_winnings(), 5905)

if __name__ == '__main__':
    main()

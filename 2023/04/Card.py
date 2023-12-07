class Card:
    """
    A simple card class to isolate operations.
    """

    def __init__(self, winning_numbers, numbers):
        # List of winning numbers
        self.winning_numbers = winning_numbers
        # List of numbers on the card
        self.numbers = numbers
        # Card score (i.e. the amount of winning_numbers found inside numbers)
        self.score = None

    def get_score(self):
        if self.score is None:
            self.score = len([n for n in self.numbers if n in
                              self.winning_numbers])
        return self.score

import unittest

class CardTest(unittest.TestCase):
    def test_score(self):
        card = Card([1, 2, 3], [4, 5, 6])
        self.assertEqual(card.get_score(), 0)

        card = Card([41, 48, 83, 86, 17], [83, 86, 6, 31, 17, 9, 48, 53])
        self.assertEqual(card.get_score(), 4)

    def test_no_winning_numbers(self):
        card = Card([], [4, 5, 6])
        self.assertEqual(card.get_score(), 0)

    def test_no_numbers(self):
        card = Card([1, 2, 3], [])
        self.assertEqual(card.get_score(), 0)

    def test_nothing(self):
        card = Card([], [])
        self.assertEqual(card.get_score(), 0)

if __name__ == '__main__':
    unittest.main()

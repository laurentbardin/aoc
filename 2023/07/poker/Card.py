import unittest

class Card:

    def __init__(self, label, joker = True):
        assert label in 'AKQJT98765432'

        self.label = label
        match label:
            case 'A':
                self.value = 14
            case 'K':
                self.value = 13
            case 'Q':
                self.value = 12
            case 'J':
                if joker:
                    self.value = 1
                else:
                    self.value = 11
            case 'T':
                self.value = 10
            case _:
                self.value = int(label)

    def __str__(self):
        return self.label
    def __repr__(self):
        return f'{self.label} ({self.value})'

    def __eq__(self, other):
        return self.label == other.label
    def __ne__(self, other):
        return self.label != other.label

    def __lt__(self, other):
        return self.value < other.value
    def __le__(self, other):
        return self.value <= other.value
    def __gt__(self, other):
        return self.value > other.value
    def __ge__(self, other):
        return self.value >= other.value

class TestCard(unittest.TestCase):

    def test_card_sort(self):
        cards = [Card('A'), Card('2'), Card('T'), Card('8'), Card('Q')]
        cards.sort()
        self.assertListEqual(cards, [Card('2'), Card('8'), Card('T'), Card('Q'), Card('A')])

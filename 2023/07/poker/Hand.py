import unittest

from .Card import Card

class Hand:

    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_KIND = 3
    FULL_HOUSE = 4
    FOUR_KIND = 5
    FIVE_KIND = 6

    def __init__(self, hand, bid = 0):
        assert(len(hand) == 5)

        self.hand = hand.upper()
        self.cards = [Card(char) for char in self.hand]
        self.type = self.get_type()

        self.bid = int(bid)

    def get_type(self):
        """
        Determine the type of the hand (i.e. its strength). We count the number
        of occurences of each card and get a sorted tuple of the number of
        occurences:

        (1, 1, 1, 1, 1) => High card
        (1, 1, 1, 2) => Pair
        (1, 2, 2) => Two pairs
        (1, 1, 3) => Three of a kind
        (2, 3) => Full house
        (1, 4) => Four of a kind
        (5, ) => Five of a kind
        """
        occurences = dict()
        for card in self.hand:
            if card in occurences:
                occurences[card] += 1
            else:
                occurences[card] = 1

        occurences = list(occurences.values())
        occurences.sort()
        match tuple(occurences):
            case (1, 1, 1, 1, 1):
                return self.HIGH_CARD
            case (1, 1, 1, 2):
                return self.PAIR
            case (1, 2, 2):
                return self.TWO_PAIR
            case (1, 1, 3):
                return self.THREE_KIND
            case (2, 3):
                return self.FULL_HOUSE
            case (1, 4):
                return self.FOUR_KIND
            case (5, ):
                return self.FIVE_KIND

    def __str__(self):
        return self.hand
    def __repr__(self):
        return f'{self.hand} ({self.bid})'

    def __eq__(self, other):
        return self.cards == other.cards
    def __lt__(self, other):
        if self.type < other.type:
            return True
        elif self.type == other.type:
            for (card, other_card) in zip(self.cards, other.cards):
                if card == other_card:
                    continue
                return card < other_card
    def __gt__(self, other):
        if self.type > other.type:
            return True
        elif self.type == other.type:
            for (card, other_card) in zip(self.cards, other.cards):
                if card == other_card:
                    continue
                return card > other_card
    def __le__(self, other):
        return self == other or self < other
    def __ge__(self, other):
        return self == other or self > other

class TestHand(unittest.TestCase):

    def test_hand_representation(self):
        self.assertEqual(str(Hand('23kKt')), '23KKT')

    def test_hand_ranking(self):
        self.assertEqual(Hand('32T3K').type, Hand.PAIR)
        self.assertEqual(Hand('KTJJT').type, Hand.TWO_PAIR)
        self.assertEqual(Hand('T55J5').type, Hand.THREE_KIND)
        self.assertEqual(Hand('JQQQJ').type, Hand.FULL_HOUSE)

    def test_hand_ordering(self):
        self.assertTrue(Hand('2AAAA') < Hand('33332'))
        self.assertTrue(Hand('2AAAA') == Hand('2AAAA'))
        self.assertTrue(Hand('2AAAA') <= Hand('2AAAA'))
        self.assertFalse(Hand('2AAAA') == Hand('33332'))
        self.assertFalse(Hand('2AAAA') > Hand('33332'))

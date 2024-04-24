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
        self.value = sum([card.value for card in self.cards])
        self.type = self.get_type()

        self.bid = bid

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

    def __eq__(self, other):
        return self.cards == other.cards
    def __lt__(self, other):
        if self.type < other.type:
            return True
        elif self.type == other.type:
            for (card, other_card) in zip(self.cards, other.cards):
                pass
    def __gt__(self, hand):
        pass

class TestHand(unittest.TestCase):

    def test_hand_representation(self):
        self.assertEqual(str(Hand('23kKt')), '23KKT')

    def test_hand_ranking(self):
        self.assertEqual(Hand('32T3K').type, Hand.PAIR)
        self.assertEqual(Hand('KTJJT').type, Hand.TWO_PAIR)

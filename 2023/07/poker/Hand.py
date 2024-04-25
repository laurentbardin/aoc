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

    def __init__(self, hand, bid = 0, joker_mode = False):
        assert(len(hand) == 5)

        self.bid = int(bid)
        self.joker_mode = joker_mode

        self.hand = hand.upper()
        self.cards = [Card(char, joker_mode) for char in self.hand]
        self.type = self.get_type()

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

        card_groups = list(occurences.values())
        card_groups.sort()
        match tuple(card_groups):
            case (1, 1, 1, 1, 1):
                if self.joker_mode and 'J' in self.hand:
                    return self.PAIR
                else:
                    return self.HIGH_CARD
            case (1, 1, 1, 2):
                if self.joker_mode and 'J' in self.hand:
                    return self.THREE_KIND
                else:
                    return self.PAIR
            case (1, 2, 2):
                if self.joker_mode and 'J' in self.hand:
                    if occurences['J'] == 1:
                        return self.FULL_HOUSE
                    else:
                        return self.FOUR_KIND
                else:
                    return self.TWO_PAIR
            case (1, 1, 3):
                if self.joker_mode and 'J' in self.hand:
                    return self.FOUR_KIND
                else:
                    return self.THREE_KIND
            case (2, 3):
                if self.joker_mode and 'J' in self.hand:
                    return self.FIVE_KIND
                else:
                    return self.FULL_HOUSE
            case (1, 4):
                if self.joker_mode and 'J' in self.hand:
                    return self.FIVE_KIND
                else:
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
        self.assertEqual(Hand('32T4J').type, Hand.HIGH_CARD)
        self.assertEqual(Hand('32J3K').type, Hand.PAIR)
        self.assertEqual(Hand('32JJK').type, Hand.PAIR)
        self.assertEqual(Hand('KTJJT').type, Hand.TWO_PAIR)
        self.assertEqual(Hand('KTKJT').type, Hand.TWO_PAIR)
        self.assertEqual(Hand('T55J5').type, Hand.THREE_KIND)
        self.assertEqual(Hand('JQQQJ').type, Hand.FULL_HOUSE)
        self.assertEqual(Hand('JQQQQ').type, Hand.FOUR_KIND)

    def test_hand_ranking_with_joker(self):
        self.assertEqual(Hand('32T4J', 0, True).type, Hand.PAIR)
        self.assertEqual(Hand('32J3K', 0, True).type, Hand.THREE_KIND)
        self.assertEqual(Hand('32JJK', 0, True).type, Hand.THREE_KIND)
        self.assertEqual(Hand('KTJJT', 0, True).type, Hand.FOUR_KIND)
        self.assertEqual(Hand('KTKJT', 0, True).type, Hand.FULL_HOUSE)
        self.assertEqual(Hand('T55J5', 0, True).type, Hand.FOUR_KIND)
        self.assertEqual(Hand('JQQQJ', 0, True).type, Hand.FIVE_KIND)
        self.assertEqual(Hand('JQQQQ', 0, True).type, Hand.FIVE_KIND)

    def test_hand_ordering(self):
        self.assertTrue(Hand('2AAAA') < Hand('33332'))
        self.assertTrue(Hand('2AAAA') == Hand('2AAAA'))
        self.assertTrue(Hand('2AAAA') <= Hand('2AAAA'))
        self.assertFalse(Hand('2AAAA') == Hand('33332'))
        self.assertFalse(Hand('2AAAA') > Hand('33332'))

    def test_hand_ordering_with_joker(self):
        self.assertTrue(Hand('T55J5', 0, True) < Hand('QQQJA', 0, True))
        self.assertTrue(Hand('QQQJA', 0, True) < Hand('KTJJT', 0, True))

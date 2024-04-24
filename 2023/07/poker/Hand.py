class Hand:

    def __init__(self, cards, bet):
        assert(len(cards) == 5) 
        self.cards = cards
        self.bet = bet
        self.rank = None

    def __str__(self):
        return self.cards

    def __eq__(self, hand):
        return self.cards == hand.cards

    def __lt__(self, hand):
        pass

    def __gt__(self, hand):
        pass

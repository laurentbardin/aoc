#!/usr/bin/env python3

from Card import Card

# Original cards
base_cards = []

# Extra cards obtained from winning original cards
extra_cards = dict()

def main():
    with open('data.txt') as cards:
        for line, card in enumerate(cards):

            (winning_numbers, numbers) = card.strip('\n').split(':')[1].split('|')
            winning_numbers = [n for n in winning_numbers.strip().split()]
            numbers = [n for n in numbers.strip().split()]

            base_cards.append(Card(winning_numbers, numbers))

    for idx, card in enumerate(base_cards):
        #print(f'Card {idx + 1}: {card.get_score()} winning numbers')
        score = card.get_score()

        if idx not in extra_cards:
            extra_cards[idx] = 0

        for i in range(idx + 1, idx + 1 + score):
            if i in extra_cards:
                extra_cards[i] += 1 + extra_cards[idx]
            else:
                extra_cards[i] = 1 + extra_cards[idx]
        #print('Current extra cards:', extra_cards)

    #print('Final extra cards:', extra_cards)

    print('Total scratchards:', sum(extra_cards.values()) + len(base_cards))


# Keep track of how many we have of each card
#cards_count = dict()
#
#last_card = None
#
#def main():
#    with open('data.txt') as cards:
#        for line, card in enumerate(cards):
#            last_card = line
#
#            if line in cards_count:
#                cards_count[line] += 1
#            else:
#                cards_count[line] = 1
#
#            (winning_numbers, numbers) = card.strip('\n').split(':')[1].split('|')
#            winning_numbers = [n for n in winning_numbers.strip().split()]
#            numbers = [n for n in numbers.strip().split() if n in
#                       winning_numbers]
#
#            start = line + 1
#            end = start + len(numbers)
#            for card in range(start, end):
#                if card in cards_count:
#                    cards_count[card] += cards_count[line]
#                else:
#                    cards_count[card] = 1
#
#    print(cards_count)
#    print('Total number of cards:', sum([v for k, v in cards_count.items() if k
#                                          <= last_card + 1]))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

def main():
    card_points = []
    with open('data.txt') as cards:
        for line, card in enumerate(cards):
            (winning_numbers, numbers) = card.strip('\n').split(':')[1].split('|')
            winning_numbers = [n for n in winning_numbers.strip().split()]
            numbers = [n for n in numbers.strip().split() if n in
                       winning_numbers]

            count = len(numbers)
            if count > 0:
                card_points.append(2**(count-1))

    print('Total points: ', sum(card_points))

if __name__ == '__main__':
    main()

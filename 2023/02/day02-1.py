#!/usr/bin/env python3

max_cubes = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

possible_games = []

def parse_sets(sets: str) -> bool:
    for cube_sets in sets.strip().split(';'):
        for cubes in cube_sets.strip().split(','):
            for (number, color) in dict([cubes.strip().split(' ')]).items():
                if (int(number) > max_cubes[color]):
                    return False

    return True

with open('data-1.txt', 'r') as content:
    for line in content:
        (game, sets) = line.split(':')
        if parse_sets(sets):
            (_, game) = game.split(' ')
            possible_games.append(int(game))

print('Sum of the IDs of possible games:', sum(possible_games))

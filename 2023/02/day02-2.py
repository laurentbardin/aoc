#!/usr/bin/env python3

max_cubes = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

game_powers = []

def compute_game_power(sets: str) -> int:
    # Minimum necessary amount of each cube
    red, green, blue = 0, 0, 0
    for cube_sets in sets.strip().split(';'):
        for cubes in cube_sets.strip().split(','):
            for (number, color) in dict([cubes.strip().split(' ')]).items():
                match color:
                    case 'red':
                        red = max(red, int(number))
                    case 'green':
                        green = max(green, int(number))
                    case 'blue':
                        blue = max(blue, int(number))
                    case _:
                        pass

    return red * green * blue

with open('data-1.txt', 'r') as content:
    for line in content:
        (game, sets) = line.split(':')
        power = compute_game_power(sets)
        game_powers.append(power)

print('Sum of the power of all games:', sum(game_powers))

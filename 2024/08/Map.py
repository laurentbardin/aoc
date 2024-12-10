import re

from itertools import combinations

class Map:
    def __init__(self, filename):
        self.antennas = dict()

        try:
            with open(filename, 'r') as file:
                antenna = re.compile(r"([a-z0-9])", re.IGNORECASE)
                for (y, line) in enumerate(file):
                    line = line.strip()
                    self.width = len(line)
                    self.height = y + 1

                    for m in antenna.finditer(line):
                        frequency = m.group(0)
                        if frequency not in self.antennas:
                            self.antennas[frequency] = set()
                        
                        self.antennas[frequency].add((m.start(), y))

        except OSError as e:
            print(f"Error reading {filename}: {e.strerror}")
            raise e

    def count_antinodes(self):
        self.antinodes = set()

        for (freq, antennas) in self.antennas.items():
            for (a, b) in combinations(antennas, 2):
                """ Distance FROM a TO b """
                distance = (b[0] - a[0], b[1] - a[1])

                antinode_a = (a[0] - distance[0], a[1] - distance[1])
                antinode_b = (b[0] + distance[0], b[1] + distance[1])
                if 0 <= antinode_a[0] < self.width and 0 <= antinode_a[1] < self.height:
                    self.antinodes.add(antinode_a)
                if 0 <= antinode_b[0] < self.width and 0 <= antinode_b[1] < self.height:
                    self.antinodes.add(antinode_b)

        return len(self.antinodes)

    def count_antinodes_with_resonance(self):
        self.antinodes = set()

        for (freq, antennas) in self.antennas.items():
            for (a, b) in combinations(antennas, 2):
                """ Distance FROM a TO b """
                distance = (b[0] - a[0], b[1] - a[1])

                """ From a first """
                is_inside = True
                while is_inside:
                    self.antinodes.add(a)
                    antinode_a = (a[0] - distance[0], a[1] - distance[1])
                    if 0 <= antinode_a[0] < self.width and 0 <= antinode_a[1] < self.height:
                        a = antinode_a
                    else:
                        is_inside = False

                """ And then from b """
                is_inside = True
                while is_inside:
                    self.antinodes.add(b)
                    antinode_b = (b[0] + distance[0], b[1] + distance[1])
                    if 0 <= antinode_b[0] < self.width and 0 <= antinode_b[1] < self.height:
                        b = antinode_b
                    else:
                        is_inside = False

        return len(self.antinodes)

import re

class Almanac:
    """
    A class to hold almanac information, parsed from an input file.
    """

    SEED = 0
    SOIL = 1
    FERTILIZER = 2
    WATER = 3
    LIGHT = 4
    TEMPERATURE = 5
    HUMIDITY = 6

    almanac = None
    map_re = re.compile(r"([a-z]+)-to-([a-z]+) map:")

    def __init__(self, file):
        self.almanac = file

        self.seeds = []
        self.locations = []
        self.seed_to_soil = []
        self.soil_to_fertilizer = []
        self.fertilizer_to_water = []
        self.water_to_light = []
        self.light_to_temperature = []
        self.temperature_to_humidity = []
        self.humidity_to_location = []

        self.parse_almanac()

    def parse_almanac(self):
        if self.almanac is None:
            return

        with open(self.almanac, 'r') as lines:
            for (line, data) in enumerate(lines):
                data = data.splitlines()[0]
                if data == '': # Blank lines
                    continue

                if data.startswith('seeds:'):
                    self.seeds = [int(s) for s in data.split(':')[1].split()]
                else:
                    match self.map_re.findall(data):
                        case [(source, destination)]:
                            self.current_source = source
                            self.current_destination = destination
                        case _:
                            self.parse_map(data)

    def parse_map(self, data):
        # Data order is "destination_start source_start range"
        (dest, src, rg) = data.split()

        # Put them in a more natural order based on the property name
        prop = self.current_source + '_to_' + self.current_destination
        self.__dict__[prop].append((int(src), int(dest), int(rg)))

    def get_locations(self):
        for seed in self.seeds:
            self.locations.append(self.find_location(self.SEED, seed))
        return self.locations

    def find_location(self, kind, value):
        """
        This method recursively finds the location of a given seed.
        """
        if kind is None:
            return value

        next_kind = None
        prop = ''

        match kind:
            case self.SEED:
                next_kind = self.SOIL
                prop = 'seed_to_soil'
            case self.SOIL:
                next_kind = self.FERTILIZER
                prop = 'soil_to_fertilizer'
            case self.FERTILIZER:
                next_kind = self.WATER
                prop = 'fertilizer_to_water'
            case self.WATER:
                next_kind = self.LIGHT
                prop = 'water_to_light'
            case self.LIGHT:
                next_kind = self.TEMPERATURE
                prop = 'light_to_temperature'
            case self.TEMPERATURE:
                next_kind = self.HUMIDITY
                prop = 'temperature_to_humidity'
            case self.HUMIDITY:
                prop = 'humidity_to_location'

        for (src, dest, rg) in self.__dict__[prop]:
            if value in range(src, src + rg):
                next_value = dest + value - src
                break
        else:
            # No mapping found so the value of src and dest are the same
            next_value = value

        return self.find_location(next_kind, next_value)

import unittest

class TestAlmanac(unittest.TestCase):
    almanac = None

    @classmethod
    def setUpClass(cls):
        cls.almanac = Almanac('example-1.txt')

    def test_seeds(self):
        self.assertListEqual(self.almanac.seeds, [79, 14, 55, 13])

    def test_maps(self):
        self.assertListEqual(self.almanac.seed_to_soil,
                             [(98, 50, 2), (50, 52, 48)])
        self.assertListEqual(self.almanac.soil_to_fertilizer,
                             [(15, 0, 37), (52, 37, 2), (0, 39, 15)])
        self.assertListEqual(self.almanac.fertilizer_to_water,
                             [(53, 49, 8), (11, 0, 42), (0, 42, 7), (7, 57, 4)])
        self.assertListEqual(self.almanac.water_to_light,
                             [(18, 88, 7), (25, 18, 70)])
        self.assertListEqual(self.almanac.light_to_temperature,
                             [(77, 45, 23), (45, 81, 19), (64, 68, 13)])
        self.assertListEqual(self.almanac.temperature_to_humidity,
                             [(69, 0, 1), (0, 1, 69)])
        self.assertListEqual(self.almanac.humidity_to_location,
                             [(56, 60, 37), (93, 56, 4)])

    def test_mappings(self):
        self.assertListEqual(self.almanac.get_locations(), [82, 43, 86, 35])

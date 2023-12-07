from itertools import batched

class SeedGenerator:
    """
    A class to generate a list of seeds. It has two modes:

        - given a list of seeds, return each one after the other. (default mode)
        - given a list of seed starting value and a range, yield each seed in
          sequence. More than one (value, range) can be provided and the generator
          will switch to the next series of seeds automatically. (range mode)
    """

    range_mode = False

    def __init__(self, mode = 'default'):
        self.seeds = []

        if mode == 'range':
            self.range_mode = True

    def get_seed(self):
        if not self.range_mode:
            for s in self.seeds:
                yield s
        else:
            for (start, length) in batched(self.seeds, 2):
                for s in range(start, start + length):
                    yield s

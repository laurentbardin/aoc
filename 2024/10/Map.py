class Map:
    topography = []

    def __init__(self, file):
        for (_, data) in enumerate(file):
            data = data.strip()
            self.topography.append(data)

        self.height = len(self.topography)
        self.width = len(self.topography[0])

    def slope_at(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            # Used in some examples to more easily check for correctness
            if self.topography[y][x] == '.':
                return float('inf')
            return int(self.topography[y][x])

        return None

    def find_zeroes(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.slope_at(x, y) == 0:
                    yield (x, y)

    def walk_trail(self, x, y):
        """
        Recursively walk a trail until we hit a valid 9 slope. Return the
        coordinates of the reached trailend.
        """
        current = self.slope_at(x, y)
        if current is not None:
            for (next_x, next_y) in [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]:
                neighbour = self.slope_at(next_x, next_y)
                if neighbour is None:
                    #print(f"Invalid neighbour at ({next_x},{next_y})")
                    continue

                if neighbour - current == 1:
                    if neighbour == 9:
                        #print(f"Found trail end at {neighbour} @ ({next_x},{next_y})")
                        yield (next_x, next_y)
                    else:
                        #print(f"Continuing trail from {neighbour} @ ({next_x},{next_y})")
                        yield from self.walk_trail(next_x, next_y)


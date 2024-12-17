from Region import Region

class Garden:

    def __init__(self, file):
        self.plots = []
        for (_, data) in enumerate(file):
            data = data.strip()
            self.plots.append(data)

        self.regions = []
        self.visited_plots = set()

        self.height = len(self.plots)
        self.width = len(self.plots[0])

    def plot_at(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.plots[y][x]

        return None

    def find_regions(self):
        for y in range(self.height):
            #print(f"Analyzing line {self.plots[y]}")
            for x in range(self.width):
                if (x, y) in self.visited_plots:
                    #print(f"Plot ({x},{y}) already visited, skipping")
                    continue

                region = Region(self.plot_at(x, y), 1, 0)
                #print(f"Starting new region for plant {region.plant} @ ({x},{y})")
                self.visited_plots.add((x, y))
                self.build_region(region, x, y)

                #print(f"Finished region: plant {region.plant}, area {region.area}, perimeter {region.perimeter}")
                self.regions.append(region)

    def price(self):
        price = 0

        for region in self.regions:
            price += region.price()

        return price

    def build_region(self, region, x, y):
        """
        Recursively build a plot region, walking into the plots of the same
        plant. This allow us to progressively build the region's area and
        perimeter, if somewhat a bit brute-forcefully.
        """
        for (next_x, next_y) in [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]:
            neighbour = self.plot_at(next_x, next_y)
            if neighbour is None or neighbour != region.plant:
                #print(f"Invalid neighbour at ({next_x},{next_y})")
                region.perimeter += 1
                continue

            if neighbour == region.plant and (next_x, next_y) not in self.visited_plots:
                region.area += 1
                self.visited_plots.add((next_x, next_y))
                self.build_region(region, next_x, next_y)


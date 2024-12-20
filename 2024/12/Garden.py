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

                region = Region(self.plot_at(x, y))
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

    def price_with_discount(self):
        price = 0

        for region in self.regions:
            self.count_sides(region)
            price += region.price_with_discount()

        return price

    def print_region(self, region):
        for y in range(region.min_y, region.max_y + 1):
            for x in range(region.min_x, region.max_x + 1):
                if self.plot_at(x, y) == region.plant:
                    print(region.plant, end='')
                else:
                    print('.', end='')
            print()

    def build_region(self, region, x, y):
        """
        Recursively build a plot region, walking into the plots of the same
        plant. This allow us to progressively build the region's area and
        perimeter, if somewhat a bit brute-forcefully.
        """
        assert(self.plot_at(x, y) == region.plant)
        region.add_plot(x, y)

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

    def count_sides(self, region):
        """
        Count sides by scanning the region horizontally and vertically.
        """
        # Convenient optimization for regions which are a simple line or column
        # (or a lone plot)
        if region.min_y == region.max_y or region.min_x == region.max_x:
            region.sides = 4
        else:
            self.count_horizontal_sides(region)
            self.count_vertical_sides(region)

    def count_horizontal_sides(self, region):
        for y in range(region.min_y, region.max_y + 1):
            fence_up = False
            fence_down = False
            for x in range(region.min_x, region.max_x + 1):
                if region.has_plot(x, y):
                    fence_up = self.look_up(region, fence_up, x, y)
                    fence_down = self.look_down(region, fence_down, x, y)
                else:
                    # Reset fences so the next plot can start counting properly
                    fence_up = False
                    fence_down = False


    def look_up(self, region, fence_up, x, y):
        plant_up = self.plot_at(x, y - 1)
        if plant_up == region.plant:
            return False
        elif not fence_up:
            region.sides += 1
            return True

        return fence_up

    def look_down(self, region, fence_down, x, y):
        plant_down = self.plot_at(x, y + 1)
        if plant_down == region.plant:
            return False
        elif not fence_down:
            region.sides += 1
            return True

        return fence_down

    def count_vertical_sides(self, region):
        for x in range(region.min_x, region.max_x + 1):
            fence_left = False
            fence_right = False
            for y in range(region.min_y, region.max_y + 1):
                if region.has_plot(x, y):
                    fence_left = self.look_left(region, fence_left, x, y)
                    fence_right = self.look_right(region, fence_right, x, y)
                else:
                    # Reset fences so the next plot can start counting properly
                    fence_left = False
                    fence_right = False

    def look_left(self, region, fence_left, x, y):
        plant_left = self.plot_at(x - 1, y)
        if plant_left == region.plant:
            return False
        elif not fence_left:
            region.sides += 1
            return True

        return fence_left

    def look_right(self, region, fence_right, x, y):
        plant_right = self.plot_at(x + 1, y)
        if plant_right == region.plant:
            return False
        elif not fence_right:
            region.sides += 1
            return True

        return fence_right

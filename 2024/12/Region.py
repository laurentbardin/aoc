from dataclasses import dataclass, field

@dataclass
class Region:
    plant: str
    area: int = field(default=1)
    perimeter: int = field(default=0)
    sides: int = field(default=0)

    # Region bounding box
    max_x: int = field(init=False)
    min_x: int = field(init=False)
    max_y: int = field(init=False)
    min_y: int = field(init=False)

    def __post_init__(self):
        # This may make some type checkers uncomfortable
        self.max_x = -float('inf')
        self.min_x = float('inf')
        self.max_y = -float('inf')
        self.min_y = float('inf')

        self.plots = set()

    def price(self):
        return self.area * self.perimeter

    def price_with_discount(self):
        return self.area * self.sides

    def add_plot(self, x, y):
        self.plots.add((x, y))
        self.update_bounding_box(x, y)

    def has_plot(self, x, y):
        return (x, y) in self.plots

    def bounding_box(self):
        return f"{self.plant}: ({self.min_x},{self.min_y}) -> ({self.max_x},{self.max_y})"

    def update_bounding_box(self, x, y):
        if x > self.max_x:
            self.max_x = x
        if x < self.min_x:
            self.min_x = x
        if y > self.max_y:
            self.max_y = y
        if y < self.min_y:
            self.min_y = y

        assert(self.max_x >= self.min_x)
        assert(self.max_y >= self.min_y)

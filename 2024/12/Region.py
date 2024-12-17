from dataclasses import dataclass

@dataclass
class Region:
    plant: str
    area: int
    perimeter: int

    def price(self):
        return self.area * self.perimeter

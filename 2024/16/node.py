class Node(object):
    def __init__(self, position):
        self.position = position

        self.parent = None

        self.g = float('inf')
        self.h = 0
        self.f = 0

        # The direction when entering the node
        self.direction = '*'

    def __str__(self):
        return f"{self.position}"

    def __eq__(self, other):
        x, y = self.position
        ox, oy = other.position
        return x == ox and y == oy
    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return self.f > other.f
    def __lt__(self, other):
        return self.f < other.f
    def __ge__(self, other):
        return self.f >= other.f
    def __le__(self, other):
        return self.f <= other.f

    def manhattan(self, dest):
        """
        Calculate the estimated cost of moving from self to dest (usually the
        goal node). If the direction is not available, print a warning.
        """
        distance = 0

        x, y = self.position
        dest_x, dest_y = dest.position
        dx, dy = x - dest_x, y - dest_y
        if self.direction is None:
            print(f"Warning: direction for node {self} is not set, h-value will not be reliable!")
        else:
            if dx == 0:
                # We're on the same column
                if self.direction in '<>':
                    distance += 1000
                elif self.direction == 'v':
                    # We'll never be above the goal node, so we're not testing for it.
                    distance += 2000
            elif dy == 0:
                # We're on the same line
                if self.direction in '^v':
                    distance += 1000
                elif self.direction == '<':
                    # We'll never be right of the goal node, so we're not testing for it.
                    distance += 2000
            else:
                # We're to the left of and below the goal node
                if self.direction in '^>':
                    distance += 1000
                else:
                    # We have to turn twice
                    distance += 2000

        return distance + abs(dx) + abs(dy)

    def cost(self, neighbour_position):
        """
        Calculate the cost (g) of moving FROM this node TO neighbour_position,
        taking the current direction into account.
        """
        cost = 1

        x, y = self.position
        nx, ny = neighbour_position

        # If we're on the same column but facing left or right, or on the same
        # line but facing up or down, we have to turn
        if x == nx and self.direction in '<>' or \
           y == ny and self.direction in '^v':
            cost += 1000

        return cost


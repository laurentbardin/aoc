class Node(object):
    def __init__(self, position):
        self.position = position

        self.parent = None

        self.g = float('inf')
        self.h = 0
        self.f = 0

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
        goal node).
        """
        x, y = self.position
        dest_x, dest_y = dest.position
        dx, dy = x - dest_x, y - dest_y

        return abs(dx) + abs(dy)

    def cost(self, neighbour_position):
        """
        Without a direction, the cost of moving from the current node to
        neighbour_position is a constant.
        """
        return 1

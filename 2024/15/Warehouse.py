from dataclasses import dataclass

class Warehouse:
    def __init__(self, data):
        self.width = len(data[0])
        self.height = len(data)

        self.robot = None
        self.objects = dict()
        for (y, line) in enumerate(data):
            for (x, obj) in enumerate(line):
                thing = None

                match obj:
                    case '#':
                        thing = Wall(x, y)
                    case 'O':
                        thing = Box(x, y)
                    case '@':
                        # Keep a handle on the robot so that we don't have to
                        # find it in the objects dict every time we need to
                        # move it
                        self.robot = Robot(x, y)
                        thing = self.robot

                if thing is not None:
                    self.objects[(x, y)] = thing

    def move_robot(self, direction):
        assert self.robot is not None

        objects = self.gather_objects(self.robot.x, self.robot.y, direction)
        # Move objects in reverse order or the coordinates will be messed up
        for obj in reversed(objects):
            del self.objects[(obj.x, obj.y)]
            obj.move(direction)
            self.objects[(obj.x, obj.y)] = obj

    """
    Gather objects in direction, starting from (x, y), which should be the
    coordinates of the robot. Stops as soon as an empty place is found,
    returning the list of movable objects. If we hit a wall before that, return
    an empty array (as nothing can be moved in that direction).
    """
    def gather_objects(self, x, y, direction):
        objects = []

        while self.objects.get((x, y)) is not None:
            obj = self.objects.get((x, y))
            if isinstance(obj, Wall):
                objects = []
                break

            objects.append(obj)
            match direction:
                case '^':
                    y -= 1
                case '>':
                    x += 1
                case 'v':
                    y += 1
                case '<':
                    x -= 1

        return objects

    def sum_gps_coordinates(self):
        coordinates = []

        for obj in self.objects.values():
            coordinates.append(obj.get_gps_coordinates())

        return sum(coordinates)

    def print(self, legend=''):
        warehouse = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for obj in self.objects.values():
            warehouse[obj.y][obj.x] = f"{obj}"

        for line in warehouse:
            print(''.join(map(str, line)))
        if legend:
            print(legend)

@dataclass
class Object:
    x: int
    y: int

    def move(self, direction):
        match direction:
            case '^':
                self.y -= 1
            case '>':
                self.x += 1
            case 'v':
                self.y += 1
            case '<':
                self.x -= 1

    def get_gps_coordinates(self):
        return 0

class Robot(Object):
    def __str__(self):
        return "@"

class Box(Object):
    def __str__(self):
        return "O"

    def get_gps_coordinates(self):
        return self.y * 100 + self.x

class Wall(Object):
    def __str__(self):
        return '#'

    def move(self, direction):
        pass

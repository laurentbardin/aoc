class Warehouse:
    def __init__(self, data):
        self.width = len(data[0]) * 2
        self.height = len(data)

        self.movements = 0

        self.robot = None
        self.objects = dict()
        for (y, line) in enumerate(data):
            for (x, obj) in enumerate(line):
                thing = None
                coords = ((x*2, x*2+1), y)
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
                        coords = (x*2, y)

                if thing is not None:
                    self.objects[coords] = thing

    def move_robot(self, direction):
        assert self.robot is not None

        self.movements += 1
        objects = self.gather_objects(self.robot, direction)

        # Move objects in reverse order or the coordinates will be messed up
        for obj in reversed(objects):
            del self.objects[(obj.x, obj.y)]
            obj.move(direction)
            self.objects[(obj.x, obj.y)] = obj

    """
    Gather objects in direction, starting from the robot. Stops as soon as an
    empty place is found, returning the list of movable objects. If we hit a
    wall before that, return an empty array (as nothing can be moved in that
    direction).
    In "wide mode", horizontal movement is fairly easy, whereas a vertical one
    is tricky: the robot can only ever push one box, but that box could push
    two, those two could push three, etc. We have to widen the search of
    objects every time we hit a box by looking at any other boxes in contact
    with the previously detected boxes.
    """
    def gather_objects(self, robot, direction):
        objects = []

        match direction:
            case '<' | '>':
                objects += self.gather_objects_horizontally(robot, direction)
            case '^' | 'v':
                objects += self.gather_objects_vertically(robot, direction)

        return objects

    def gather_objects_horizontally(self, robot, direction):
        objects = [robot]

        match direction:
            case '>':
                next_x = robot.get_right_neighbour_x()
            case '<':
                next_x = robot.get_left_neighbour_x()
            case _:
                raise ValueError("Invalid horizontal direction '{direction}'")

        next_object = self.objects.get((next_x, robot.y))
        while next_object is not None:

            if isinstance(next_object, Wall):
                objects = []
                break

            objects.append(next_object)
            match direction:
                case '>':
                    next_x = next_object.get_right_neighbour_x()
                case '<':
                    next_x = next_object.get_left_neighbour_x()

            next_object = self.objects.get((next_x, robot.y))

        return objects

    def gather_objects_vertically(self, robot, direction):
        objects = [robot]

        match direction:
            case '^':
                gather_func = self.find_boxes_above
            case 'v':
                gather_func = self.find_boxes_below
            case _:
                raise ValueError("Invalid vertical direction '{direction}'")

        objects += gather_func(robot)

        if any([True if isinstance(o, Wall) else False for o in objects]):
            # Found a wall
            objects = []

        return objects

    def find_boxes_above(self, obj):
        objects = []

        if obj.y == 0:
            return objects

        for next_x in obj.get_vertical_neighbours_x():
            next_object = self.objects.get((next_x, obj.y - 1))
            if next_object is not None:
                objects.append(next_object)
                objects += self.find_boxes_above(next_object)

        return objects

    def find_boxes_below(self, obj):
        objects = []

        if obj.y == self.height - 1:
            return objects

        for next_x in obj.get_vertical_neighbours_x():
            next_object = self.objects.get((next_x, obj.y + 1))
            if next_object is not None:
                objects.append(next_object)
                objects += self.find_boxes_below(next_object)

        return objects

    def sum_gps_coordinates(self):
        coordinates = []

        for obj in self.objects.values():
            coordinates.append(obj.get_gps_coordinates())

        return sum(coordinates)

    def print(self, legend=''):
        warehouse = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for obj in self.objects.values():
            s = f"{obj}"
            if isinstance(obj, Robot):
                warehouse[obj.y][obj.x] = s
            else:
                (warehouse[obj.y][obj.x[0]], warehouse[obj.y][obj.x[1]]) = (s[:1], s[1:])

        if legend:
            print(legend)
        for (n, line) in enumerate(warehouse):
            print(''.join([c for c in line]) + f" {n}")

class Object:
    def __init__(self, x, y):
        self.x = (x*2, x*2+1)
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def move(self, direction):
        match direction:
            case '^':
                self.y -= 1
            case '>':
                self.x = tuple(map(lambda x: x+1, self.x))
            case 'v':
                self.y += 1
            case '<':
                self.x = tuple(map(lambda x: x-1, self.x))

    def get_gps_coordinates(self):
        return 0

    def get_left_neighbour_x(self):
        return tuple(map(lambda x: x-2, self.x))

    def get_right_neighbour_x(self):
        return tuple(map(lambda x: x+2, self.x))

    def get_vertical_neighbours_x(self):
        return [(self.x[0]-1, self.x[0]), (self.x[0], self.x[1]), (self.x[1], self.x[1]+1)]

class Robot(Object):
    def __init__(self, x, y):
        self.x = x*2
        self.y = y

    def __str__(self):
        return "@"

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

    def get_left_neighbour_x(self):
        return tuple([self.x - 2, self.x - 1])

    def get_right_neighbour_x(self):
        return tuple([self.x + 1, self.x + 2])

    def get_vertical_neighbours_x(self):
        return [(self.x-1, self.x), (self.x, self.x+1)]

class Box(Object):
    def __str__(self):
        return "[]"

    def get_gps_coordinates(self):
        return (100 * self.y) + min(self.x)

class Wall(Object):
    def __str__(self):
        return '##'

    def move(self, direction):
        assert False, "Tried to move a wall!"

    def get_left_neighbour_x(self):
        return tuple([])

    def get_right_neighbour_x(self):
        return tuple([])

    def get_vertical_neighbours_x(self):
        return []

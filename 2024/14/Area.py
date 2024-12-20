from functools import reduce

class Area:
    def __init__(self, width=101, height=103):
        self.width = width
        self.height = height

        self.robots = []
        self.safety_factor = None

    def add_robot(self, robot):
        self.robots.append(robot)

    def simulate_robots(self, seconds=100):
        for robot in self.robots:
            final_x = robot.position[0] + (robot.velocity[0] * seconds)
            final_y = robot.position[1] + (robot.velocity[1] * seconds)
            robot.position = (final_x % self.width, final_y % self.height)
            assert(0 <= robot.position[0] < self.width)
            assert(0 <= robot.position[1] < self.height)

    def get_safety_factor(self):
        if self.safety_factor is None:
            quadrants = [0, 0, 0, 0] # Number of robots in each quadrant
            middle_x = (self.width - 1) // 2
            middle_y = (self.height - 1) // 2
            for robot in self.robots:
                if robot.is_on_column(middle_x) or robot.is_on_line(middle_y):
                    continue

                if robot.is_in_box(0, 0, middle_x - 1, middle_y - 1):
                    quadrants[0] += 1
                elif robot.is_in_box(middle_x + 1, 0, self.width - 1, middle_y - 1):
                    quadrants[1] += 1
                elif robot.is_in_box(0, middle_y + 1, middle_x -1, self.height - 1):
                    quadrants[2] += 1
                elif robot.is_in_box(middle_x + 1, middle_y + 1, self.width - 1, self.height - 1):
                    quadrants[3] += 1
                
            self.safety_factor = reduce(lambda x, y: x * y, quadrants)

        return self.safety_factor

    def print_area(self):
        area = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for robot in self.robots:
            column = robot.position[0]
            line = robot.position[1]
            if area[line][column] == '.':
                area[line][column] = 1
            else:
                area[line][column] += 1

        for line in area:
            print(''.join([c for c in map(str, line)]))

class Robot:
    def __init__(self, p, v):
        self.position = p
        self.velocity = v

    def __str__(self):
        return f"Robot @ ({self.position[0]},{self.position[1]})"

    def is_on_column(self, x):
        return self.position[0] == x

    def is_on_line(self, y):
        return self.position[1] == y

    def is_in_box(self, x1, y1, x2, y2):
        return x1 <= self.position[0] <= x2 and y1 <= self.position[1] <= y2

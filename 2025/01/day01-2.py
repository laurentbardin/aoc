import sys
import unittest

DIAL_LENGTH = 100

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    password = get_password(filename)
    print(f"Password: {password}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def count_zeroes(distance):
    zeroes = distance // DIAL_LENGTH
    distance -= zeroes * DIAL_LENGTH

    return zeroes, distance

def move_dial(position, direction, distance):
    assert 0 <= distance < DIAL_LENGTH

    pointed_to_zero = False

    if direction == 'R':
        new_position = position + distance
    else:
        new_position = position - distance

    if position > 0 and (new_position <= 0 or new_position >= DIAL_LENGTH):
        pointed_to_zero = True

    return new_position % 100, pointed_to_zero

def get_password(filename):
    position = 50
    password = 0

    try:
        with open(filename, 'r') as file:
            for rotation in file.readlines():
                direction = rotation[0]
                distance = int(rotation[1:].strip())

                zeroes, distance = count_zeroes(distance)
                position, pointed_to_zero = move_dial(position, direction, distance)

                password += zeroes
                if pointed_to_zero:
                    password += 1

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

    return password

class TestPassword(unittest.TestCase):
    def test_password(self):
        password = get_password('example.txt')
        self.assertEqual(password, 6)

    def test_left_rotation(self):
        position = 50
        distance = 40
        zeroes, distance = count_zeroes(distance)
        self.assertEqual(zeroes, 0)
        self.assertEqual(distance, 40)

        position, pointed_to_zero = move_dial(position, 'L', distance)
        self.assertEqual(position, 10)
        self.assertFalse(pointed_to_zero)

    def test_left_rotation_over_zero(self):
        position = 50
        distance = 60
        zeroes, distance = count_zeroes(distance)
        self.assertEqual(zeroes, 0)
        self.assertEqual(distance, 60)

        position, pointed_to_zero = move_dial(position, 'L', distance)
        self.assertEqual(position, 90)
        self.assertTrue(pointed_to_zero)

    def test_left_rotation_to_zero(self):
        position = 50
        distance = 50
        zeroes, distance = count_zeroes(distance)
        self.assertEqual(zeroes, 0)
        self.assertEqual(distance, 50)

        position, pointed_to_zero = move_dial(position, 'L', distance)
        self.assertEqual(position, 0)
        self.assertTrue(pointed_to_zero)

    def test_left_rotation_from_zero(self):
        position = 0
        distance = 50
        zeroes, distance = count_zeroes(distance)
        self.assertEqual(zeroes, 0)
        self.assertEqual(distance, 50)

        position, pointed_to_zero = move_dial(position, 'L', distance)
        self.assertEqual(position, 50)
        self.assertFalse(pointed_to_zero)

    def test_multiple_left_rotation(self):
        distance = 360
        zeroes, distance = count_zeroes(distance)
        self.assertEqual(zeroes, 3)
        self.assertEqual(distance, 60)

        distance = 340
        zeroes, distance = count_zeroes(distance)
        self.assertEqual(zeroes, 3)
        self.assertEqual(distance, 40)

    def test_multiple_left_rotation_to_zero(self):
        position = 50
        distance = 350
        zeroes, distance = count_zeroes(distance)
        self.assertEqual(zeroes, 3)
        self.assertEqual(distance, 50)

        position, pointed_to_zero = move_dial(position, 'L', distance)
        self.assertEqual(position, 0)
        self.assertTrue(pointed_to_zero)

    def test_right_rotation(self):
        position = 50
        distance = 40
        zeroes, distance = count_zeroes(distance)
        self.assertEqual(zeroes, 0)
        self.assertEqual(distance, 40)

        position, pointed_to_zero = move_dial(position, 'R', distance)
        self.assertEqual(position, 90)
        self.assertFalse(pointed_to_zero)

    def test_right_rotation_over_zero(self):
        position = 50
        distance = 60
        zeroes, distance = count_zeroes(distance)
        self.assertEqual(zeroes, 0)
        self.assertEqual(distance, 60)

        position, pointed_to_zero = move_dial(position, 'R', distance)
        self.assertEqual(position, 10)
        self.assertTrue(pointed_to_zero)

    def test_right_rotation_to_zero(self):
        position = 50
        distance = 50
        zeroes, distance = count_zeroes(distance)
        self.assertEqual(zeroes, 0)
        self.assertEqual(distance, 50)

        position, pointed_to_zero = move_dial(position, 'R', distance)
        self.assertEqual(position, 0)
        self.assertTrue(pointed_to_zero)

    def test_right_rotation_from_zero(self):
        position = 0
        distance = 50
        zeroes, distance = count_zeroes(distance)
        self.assertEqual(zeroes, 0)
        self.assertEqual(distance, 50)

        position, pointed_to_zero = move_dial(position, 'R', distance)
        self.assertEqual(position, 50)
        self.assertFalse(pointed_to_zero)

    def test_multiple_right_rotation(self):
        distance = 360
        zeroes, distance = count_zeroes(distance)
        self.assertEqual(zeroes, 3)
        self.assertEqual(distance, 60)

        distance = 320
        zeroes, distance = count_zeroes(distance)
        self.assertEqual(zeroes, 3)
        self.assertEqual(distance, 20)

    def test_multiple_right_rotation_to_zero(self):
        position = 50
        distance = 350
        zeroes, distance = count_zeroes(distance)
        self.assertEqual(zeroes, 3)
        self.assertEqual(distance, 50)

        position, pointed_to_zero = move_dial(position, 'R', distance)
        self.assertEqual(position, 0)
        self.assertTrue(pointed_to_zero)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

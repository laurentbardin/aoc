import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    password = get_password(filename)
    print(f"Password: {password}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def get_password(filename):
    position = 50
    password = 0

    try:
        with open(filename, 'r') as file:
            for rotation in file.readlines():
                direction = rotation[0]
                distance = int(rotation[1:].strip())

                if direction == 'R':
                    position += distance
                else:
                    position -= distance

                position %= 100

                if position == 0:
                    password += 1

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

    return password

class TestPassword(unittest.TestCase):
    def test_password(self):
        password = get_password('example.txt')
        self.assertEqual(password, 3)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

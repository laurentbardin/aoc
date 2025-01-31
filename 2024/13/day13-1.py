import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    cost = data_from_file(filename, analyze_list)
    print(f"Minimum number of tokens to spend: {cost}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def analyze_list(file):
    cost = 0

    eq = [[], []]
    for (_, line) in enumerate(file):
        line = line.splitlines()[0]
        if line.find("Button A") == 0 or line.find("Button B") == 0:
            values = [int(v.split('+')[1]) for v in line.split(':')[1].split(',')]
            eq[0].append(values[0])
            eq[1].append(values[1])
        elif line.find("Prize") == 0:
            values = [int(v.split('=')[1]) for v in line.split(':')[1].split(',')]
            eq[0].append(values[0])
            eq[1].append(values[1])
        else:
            cost += solve(eq)
            eq = [[], []]

    cost += solve(eq)
    return cost

def solve(eq):
    """
    Return the minimum nomber of tokens needed to win a given prize, if
    possible. Uses a crude linear equations solver with an array disguised as a
    matrix.
    """
    cost = 0

    m = lcm(eq[0][0], eq[1][0])
    factors = [m // eq[0][0], m // eq[1][0]]

    eq[0] = list(map(lambda x: x * factors[0], eq[0]))
    eq[1] = list(map(lambda x: x * factors[1], eq[1]))
    assert eq[0][0] == eq[1][0]

    # Check the value are actual integers and not truncated floats
    button_b = (eq[0][2] - eq[1][2]) / (eq[0][1] - eq[1][1])
    if button_b.is_integer():
        button_b = int(button_b)
        button_a = (eq[0][2] - button_b * eq[0][1]) // eq[0][0]

        if button_a < 100 and button_b < 100:
            cost = button_a * 3 + button_b

    return cost


def lcm(a, b):
    """ Return the lowest common multiple of a and b """
    return a * b // gcd(a, b)

def gcd(a, b):
    """ Return the greatest common divisor of a and b (see Euclid's Algorithm) """
    while b:
        a, b = b, a % b
    return a

def data_from_file(filename, cb):
    try:
        with open(filename, 'r') as file:
            return cb(file)

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

class TestTopography(unittest.TestCase):

    def test_claw_machine(self):
        cost = data_from_file('example-1.txt', analyze_list)
        self.assertEqual(cost, 480)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

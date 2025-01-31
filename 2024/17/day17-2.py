import sys
import unittest

from vm import vm

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    result, a = data_from_file(filename, analyze_program)
    print(f"Program output: {result}, {a=}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def analyze_program(file):
    for line in file:
        if line.find("Program") == 0:
            program = line.split(':')[1].splitlines()[0].strip()

    b = c = 0
    """
    To determine the minimum value of register A, we have to analyze the
    executed program (see input.txt). It goes like this:

    0: bst a # b = a % 8
    1: bxl 5 # b = b ^ 5
    2: cdv b # c = a // 2**b
    3: bxl 6 # b = b ^ 6
    4: bxc _ # b = b ^ c
    5: out b # b % 8
    6: adv 3 # a = a // 2**3
    7: jnz 0

    Basically, one loop iteration takes the value of A, does some operations
    with it, outputs the result, divides and truncates the value of A by 8, and
    repeats itself if A is not 0. If the target output contains n values, then
    the loop should repeat n times. To guarantee that, the value of A should be
    at least 8**(n-1) and at most (8**n)-1: these bounds are divisible by 8 n
    times in a row before reaching 0, thus enabling n loop iterations and
    therefore an output of length n.
    The goal is now to manipulate the initial value of A to produce a series of
    values that will lead to a specific output (in this case, the original
    program). We can influence the first value of the ouput by modifiying the
    initial value of A. Once we've augmented A by 8, the second loop iteration
    will have the value of A augmented by 1. If we then want A to be augmented
    by 1 for the third loop, we'll have to add at least 8 to A at the start of
    the second loop, and therefore 64 for the first one.
    It follows that in order to influence the last value, we have to add to A
    in increments of 8**(n-1), for the second to last value, increments of
    8**(n-2), etc.
    """
    expected_output = list(map(int, program.split(',')))
    #print(f"{expected_output=}")
    n = len(expected_output)

    # List of coefficients for the powers of 8:
    # coefficients[0] = i -> i * 8**0
    # coefficients[1] = j -> j * 8**1
    # ...
    # coefficients[n-1] = z -> z * 8**(n-1)
    coefficients = [0] * n
    coefficients[n-1] = 1 # The minimum to get an output of n values
    while True:
        for i in range(n - 1, -1, -1):
            while True:
                a = sum([c*8**e for e, c in enumerate(coefficients)])

                vm.reset(a, b, c, program)
                output = vm.run()
                if output[i] == expected_output[i]:
                    #print(f"{coefficients=}")
                    break

                coefficients[i] += 1

            # If a coefficient is above 8, it "spills" to the next one:
            # 10 * 8**10 + 2 * 8**11 == 2 * 8**10 + 3 * 8**11
            if coefficients[i] >= 8:
                if i == n - 1:
                    print("No value of A seems to exist to produce the desired output :(")
                    return [], None
                else:
                    coefficients[i+1] += coefficients[i] // 8
                    # Keeping the remainder (as in coefficients[i] %= 8) can
                    # give a working value for A in the end, but not the lowest
                    # one.
                    # TODO Revisit the math to try and understand why
                    coefficients[i] = 0
                    break
        else:
            break

    return ','.join(map(str, output)), a

def data_from_file(filename, cb):
    try:
        with open(filename, 'r') as file:
            return cb(file)

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

class TestProgram(unittest.TestCase):

    def test_program_output(self):
        result, a = data_from_file('example-2.txt', analyze_program)
        self.assertEqual(result, '0,3,5,4,3,0')
        self.assertEqual(a, 117440)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

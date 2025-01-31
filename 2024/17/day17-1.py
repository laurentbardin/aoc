import re
import sys
import unittest

from vm import vm

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    result = data_from_file(filename, analyze_program)
    print(f"Program output: {result}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def analyze_program(file):
    a = b = c = 0

    reg = re.compile(r"Register ([ABC]): (\d+)")
    for line in file:
        match = reg.search(line)
        if match is not None:
            register = match.group(1)
            value = int(match.group(2))
            if register == 'A':
                a = value
            elif register == 'B':
                b = value
            elif register == 'C':
                c = value
        elif line.find("Program") == 0:
            program = line.split(':')[1].splitlines()[0]

    vm.reset(a, b, c, program)

    output = vm.run()
    output = ','.join(map(str, output))

    return output

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
        result = data_from_file('example-1.txt', analyze_program)
        self.assertEqual(result, '4,6,3,5,6,3,5,2,1,0')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    paths = data_from_file(filename, count_paths)
    print(f"Number of different paths to 'out': {paths}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def data_from_file(filename, cb):
    try:
        with open(filename, 'r') as file:
            return cb(file)

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

def count_paths(file):
    devices = {}

    for line in file:
        device, outputs = line.strip().split(':')
        devices[device] = outputs.split()

    paths = walk_devices(devices, 'you')

    return paths

def walk_devices(devices, from_device):
    if from_device == 'out':
        return 1

    paths = 0
    for device in devices[from_device]:
        paths += walk_devices(devices, device)

    return paths

class TestPaths(unittest.TestCase):
    def test_paths(self):
        paths = data_from_file('example1.txt', count_paths)
        self.assertEqual(paths, 5)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

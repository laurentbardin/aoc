import sys
import unittest

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    checksum = data_from_file(filename, analyze_disk)
    print(f"Filesystem checksum: {checksum}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def analyze_disk(file):
    disk_map = file.readline().strip()

    files = build_files(disk_map)
    disk_layout = build_layout(files)

    disk_layout = defrag(disk_layout)

    return checksum(disk_layout)

def defrag(layout):
    defragged = []
    defrag_index = 0
    layout_index = len(layout) - 1

    while defrag_index <= layout_index:
        if layout[defrag_index] is not None:
            defragged.append(layout[defrag_index])
        else:
            while layout[layout_index] is None:
                layout_index -= 1
            defragged.append(layout[layout_index])
            layout_index -= 1

        defrag_index += 1

    return defragged

def checksum(layout):
    return sum([i * n for (i, n) in enumerate(layout)])

def build_files(disk_map):
    position = 0 # Starting index of the files
    file_id = 0 # Current file ID
    files = dict() # Map file ID to (position, filesize) tuple
    for (i, n) in enumerate(disk_map):
        n = int(n)
        if i % 2 == 0:
            files[file_id] = (position, n)
            file_id += 1
        position += n

    return files

def build_layout(files):
    """
    Build the layout as a long array. Index is the block ID, value is the
    file ID, or None if the block is empty. This is necessary for file IDs
    above 9 (or above 15 if we used hexadecimal)
    """
    layout = []
    layout_pos = 0

    for (file_id, file_data) in files.items():
        while layout_pos < file_data[0]:
            # Fill in with empty space first
            layout.append(None)
            layout_pos += 1

        for data in range(file_data[1]):
            layout.append(file_id)

        layout_pos += file_data[1]

    return layout

def print_layout(layout):
    """ Debug function to print the layout as a string """
    print(''.join(map(lambda i: '.' if i is None else str(i), layout)))

def data_from_file(filename, cb):
    try:
        with open(filename, 'r') as file:
            return cb(file)

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

class TestCalibration(unittest.TestCase):

    def test_checksum(self):
        checksum = data_from_file('example.txt', analyze_disk)
        self.assertEqual(checksum, 1928)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

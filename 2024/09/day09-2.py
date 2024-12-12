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

    (files, free_blocks) = build_files(disk_map)

    files = defrag(files, free_blocks)

    return checksum(files)

def defrag(files, free_blocks):
    """
    Navigate the files in reverse ID order, and try to move each of them into
    the leftmost free block that can accomodate their size.
    """
    for (file_id, file) in reversed(files.items()):
        block_position = find_free_block(free_blocks, file)
        if block_position is None:
            continue

        assert(block_position < file['position'])
        file['position'] = block_position

        # Update the free blocks data
        new_block_size = free_blocks[block_position] - file['size']
        assert(new_block_size >= 0)
        if new_block_size > 0:
            new_position = block_position + file['size']
            assert(new_position not in free_blocks)
            free_blocks[new_position] = new_block_size

        del(free_blocks[block_position])

    return files

def find_free_block(blocks, file):
    min_position = float('inf')
    for (position, size) in blocks.items():
        if size >= file['size'] and position < min_position and position < file['position']:
            min_position = position

    return min_position if min_position < float('inf') else None

def checksum(files):
    """ < 8446022420670 """
    cksum = 0
    for (file_id, file) in files.items():
        cksum += sum([file_id * pos for pos in range(file['position'], file['position'] + file['size'])])

    return cksum

def build_files(disk_map):
    position = 0 # Starting index of the files
    file_id = 0 # Current file ID
    files = dict() # Map file ID to {position, size} dict

    # Keep track of the free blocks in simple "position to size" dict
    free_blocks = dict()
    for (i, size) in enumerate(disk_map):
        size = int(size)
        if i % 2 == 0:
            files[file_id] = {'position': position, 'size': size}
            file_id += 1
        elif size > 0:
            free_blocks[position] = size

        position += size

    return (files, free_blocks)

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
        self.assertEqual(checksum, 2858)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

import sys
import unittest

ACTIVE_BATTERIES = 12
MAX_BATTERY = 9
MIN_BATTERY = 1

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    total = data_from_file(filename, get_joltage_output)
    print(f"Total joltage output: {total}")

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

def get_joltage_output(file):
    batteries = []
    for bank in file:
        positions = []
        bank = bank.strip()

        # Find the positions of the highest digits, starting from 9 and
        # counting down, until we have the desired amount of active batteries
        n = MAX_BATTERY
        while len(positions) < ACTIVE_BATTERIES and n >= MIN_BATTERY:
            target = str(n)
            if target in bank:
                for i, value in enumerate(bank):
                    if value == target:
                        positions.append(i)
                        if len(positions) >= ACTIVE_BATTERIES:
                            break

            n -= 1

        positions.sort()

        max_number = maximise(bank, positions)
        batteries.append(int(max_number))

    return sum(batteries)

def maximise(bank, positions):
    """
    Given a bank of batteries and the positions of the highest digits, try and
    maximise the value of the selected batteries by moving higher digits to the
    left as much as possible.
    """
    done = False

    while not done:
        candidate = ''.join(map(str, [bank[b] for b in positions]))

        for i, n in enumerate(candidate):
            if i < len(candidate) - 1:
                next_n = candidate[i+1]
                if next_n <= n:
                    # If the digit to the right of the current one is lower or
                    # equal, we have nothing to gain from removing it
                    continue

                # Find the best possible battery to the right of next_n in bank
                pos = None
                best = '0'
                current = positions[i+1] + 1
                while current < len(bank):
                    if current not in positions and bank[current] > best:
                        best = bank[current]
                        pos = current
                    current += 1
                else:
                    if pos is None:
                        # We reached the end of the bank without finding a
                        # potential replacement
                        continue

                # Get the corresponding index of the selected replacement in
                # bank, and swap it with the current battery
                del(positions[i])
                positions.append(pos)
                positions.sort()
                break
        else:
            done = True

    #debug_battery_bank(bank, positions)
    return candidate

def debug_battery_bank(bank, positions):
    """
    Display the selected batteries in a line above the battery bank. The latter
    contains holes where batteries have been selected.
    """
    for i, n in enumerate(bank):
        if i in positions:
            print(n, end='')
        else:
            print(' ', end='')
    print('')

    for i, n in enumerate(bank):
        if i not in positions:
            print(n, end='')
        else:
            print(' ', end='')
    print('')

class TestBatteries(unittest.TestCase):
    def test_batteries(self):
        total = data_from_file('example.txt', get_joltage_output)
        self.assertEqual(total, 3121910778619)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

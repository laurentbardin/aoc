import sys

from Area import Area, Robot

def main():
    filename = sys.argv[1]
    if not filename:
        usage()
        sys.exit(1)

    area = Area()
    safety_factor = data_from_file(filename, analyze_robots, area)
    print(f"Safety factor: {safety_factor}")

def usage():
    print(f"Usage: python {sys.argv[0]} <filename>")

def analyze_robots(file, area):
    for (_, line) in enumerate(file):
        (p, v) = line.splitlines()[0].split()
        p = tuple([int(c) for c in p.split('=')[1].split(',')])
        v = tuple([int(s) for s in v.split('=')[1].split(',')])

        area.add_robot(Robot(p, v))

    elapsed_seconds = 0

    # Strange patterns start to appear after 49 and 98 seconds...
    skip = input("Skip some simulation (leave blank for no skipping): ")
    if skip:
        try:
            skip = int(skip)
            area.simulate_robots(skip)
            elapsed_seconds = skip
        except ValueError:
            pass

    # ... and repeat themselves every 103 and 101 seconds, respectively. The
    # fact that these are the grid dimensions smells like witchcraft a bit, but
    # it leads to the solution faster than checking every second, so we'll use that.
    stepping = 1
    while True:
        area.print(f"After {elapsed_seconds} seconds")

        choice = input("Continue? [Y/n] ")
        if choice == "n":
            break

        area.simulate_robots(stepping)
        elapsed_seconds += stepping

    return area.get_safety_factor()

def data_from_file(filename, cb, area):
    try:
        with open(filename, 'r') as file:
            return cb(file, area)

    except OSError as e:
        print(f"Error reading {filename}: {e.strerror}")
        usage()
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        main()

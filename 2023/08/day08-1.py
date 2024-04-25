def main():
    (directions, nodes) = data_from_file('data.txt')

    steps = count_steps_to('ZZZ', directions, nodes)

    print(f'Number of steps to reach ZZZ: {steps}')

def data_from_file(filename):
    directions = ''
    nodes = dict()

    with open(filename, 'r') as file:
        for (line, data) in enumerate(file):
            data = data.splitlines()[0]
            if line == 0:
                directions = data.strip()
                continue

            if '=' in data:
                (node, targets) = tuple(s.strip() for s in data.split('='))
                (left, right) = tuple(t.strip('() ') for t in targets.split(','))
                nodes[node] = {'L': left, 'R': right}

    return (directions, nodes)

def count_steps_to(target, directions, nodes):
    # Sanity check
    if target not in nodes:
        print("Target doesn't exist, aborting")
        return 0

    steps = 0
    location = 'AAA'

    while location != target:
        for d in directions:
            location = nodes[location][d]
            steps += 1

            if location == target:
                break

    return steps

if __name__ == '__main__':
    main()

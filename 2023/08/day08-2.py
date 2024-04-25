def main():
    (directions, nodes) = data_from_file('data.txt')

    start_locations = [l for l in nodes if l[-1] == 'A']
    target_locations = [l for l in nodes if l[-1] == 'Z']
    # Sanity checks
    if len(target_locations) == 0:
        print("No target location available, aborting")
    else:
        #steps = count_steps_to_finish(start_locations, directions, nodes)
        steps = calculate_steps_to_finish(start_locations, directions, nodes)

        print(f'Number of steps to reach final destinations: {steps}')

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

def count_steps_to_finish(start_locations, directions, nodes):
    """
    This is the original, brute force version. It will take a very long time if
    passed all 6 starting locations.
    """
    steps = 0
    loops = 0
    final_locations = 0
    current_locations = start_locations[:]

    while final_locations != len(current_locations):
        for d in directions:
            current_locations = [nodes[l][d] for l in current_locations]
            final_locations = len([l for l in current_locations
                                   if l[-1] == 'Z'])
            steps += 1

            if final_locations == len(current_locations):
                break
        else:
            loops += 1
            if loops % 10_000 == 0:
                print('Loops', loops)

    return steps

def calculate_steps_to_finish(start_locations, directions, nodes):
    """
    This is the smart and efficient way to solve the riddle. Once you realize
    that every trip from one starting location comes around after a certain
    number of cycles, you can easily calculate the number of cycles needed for
    every trip to end at their target location simultaneously.
    """
    # Calculate the number of steps needed by each starting location to reach a
    # target location
    cycles = []
    for l in start_locations:
        steps = count_steps_to_finish([l], directions, nodes)
        cycles.append(count_steps_to_finish([l], directions, nodes) /
                     len(directions))
    total_steps = 1
    for c in cycles:
        total_steps *= int(c)

    return total_steps * len(directions)

if __name__ == '__main__':
    main()

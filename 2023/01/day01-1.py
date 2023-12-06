#!/usr/bin/env python3

calibration = []

with open('calibration-1.txt', 'r') as content:
    for line in content:

        # Search first and last digit characters
        first, last = 0, 0
        for char in line:
            if char.isdigit():
                first = char
                break
    
        for char in reversed(line):
            if char.isdigit():
                last = char
                break
    
        calibration.append(int(first + last))

print('Calibration:', sum(calibration))

#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Quick calculation of the N50 of a genome and output to terminal

import sys


sequence, lengths = [], []
with open(sys.argv[1]) as genome:
    for line in genome:
        if line.startswith('>'):
            lengths.append(len(''.join(sequence)))
            sequence = []
        else:
            sequence += line.strip()

n50 = sorted(lengths)[int(len(lengths) / 2)]

print("N50 = %s" % n50)

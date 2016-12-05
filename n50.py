#!/usr/bin/env python3

# Calculate N50 of a genome

import sys

__author__ = 'groverj3'

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

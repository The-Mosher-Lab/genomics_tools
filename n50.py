#!/usr/bin/env python3

import sys

sequence, lengths = [], []
with open(sys.argv[1]) as genome:
    for line in genome:
        if line.startswith('>'):
            lengths.append(len(''.join(sequence)))
            sequence = []
        else:
            sequence += line.strip()

n50 = sorted(lengths)[len(lengths) / 2]

print "N50 = %s" % n50
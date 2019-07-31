#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Take a .bed file with and append a number to each ID in column 4 if
# they are not unique
# Created: 11/2017

# This script originally was to uniquify TE IDs in this format:
# chr   start   stop    TE-family   TE-type strand
# But now should work with valid (and most invalid) bed files

from argparse import ArgumentParser


def uniquify_bed(input_bed):
    with open(input_bed, 'r') as input_handle:
        te_counts = {}
        for line in input_handle:
            entry = line.strip().split()
            te_id = entry[3]
            if te_id not in te_counts:
                te_counts[te_id] = 1
            else:
                te_counts[te_id] += 1
            entry[3] = '{}_{}'.format(te_id, te_counts[te_id])
            print('\t'.join(entry))


# Parse command line options

def get_args():
    parser = ArgumentParser(
        description='Take a .bed file and append a number to each ID in column '
        '4 if they are not unique')
    parser.add_argument('input_bed', help='File to process', metavar='FILE.bed')
    return parser.parse_args().input_bed


# Process the file

def main(input_file):
    uniquify_bed(input_file)


if __name__ == '__main__':
    main(get_args())

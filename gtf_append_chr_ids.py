#!/usr/bin/env python3
# Author: Jeffrey Grover
# Purpose: Append a string to all chromosome IDs
# Created: 2019-03-14

from argparse import ArgumentParser


def append_chromosome(input_file, chrom_string):
    with open(input_file, 'r') as input_handle:
        for line in input_handle:
            entry = line.strip().split('\t')
            entry[0] = entry[0] + chrom_string
            print('\t'.join(entry))


# Parse command line options

def get_args():
    parser = ArgumentParser(
        description='Appends a string to all chromosomes in a GTF file')
    parser.add_argument('gtf', help='File to process', metavar='FILE.gtf')
    parser.add_argument('--string',
                        '-s',
                        help='String to add to each chromosome ID')
    return parser.parse_args()


# Process file


def main(args):
    append_chromosome(args.gtf, args.string)


if __name__ == '__main__':
    main(get_args())

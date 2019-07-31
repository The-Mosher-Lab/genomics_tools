#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Take a file output by bedtools merge and assign IDs to the rows.
# Output a bed file with 6 columns.
# Created: 2019-04-19

from argparse import ArgumentParser


def assign_bedtools_merge(input_file, basename):
    line_count = 0
    with open(input_file, 'r') as input_handle:
        for line in input_handle:
            line_count += 1
            entry = line.strip().split()
            chromosome = entry[0]
            start = entry[1]
            stop = entry[2]
            strand = entry[3]
            name = basename + str(line_count)
            print(chromosome, start, stop, name, '.', strand, sep='\t')


# Parse command line options

def get_args():
    parser = ArgumentParser(
        description='Take the output from bedtools merge and assign unique IDs '
        'to each line')
    parser.add_argument('input_file',
                        help='File to process',
                        metavar='FILE')
    parser.add_argument('-b', '--basename',
                        help='Basename to append ID number to for each record')
    return parser.parse_args()


# Process the file

def main(args):
    assign_bedtools_merge(args.input_file, args.basename)


if __name__ == '__main__':
    main(get_args())

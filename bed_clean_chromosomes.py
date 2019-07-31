#!/usr/bin/env python3
# Author: Jeffrey Grover
# Purpose: Clean garbage from bed files in the chromosome ID fields
# Created: 09/2018

from argparse import ArgumentParser


def clean_bed(input_file, cleaner_sep):
    with open(input_file, 'r') as input_handle:
        for line in input_handle:
            entry = line.strip().split()
            entry[0] = entry[0].split(cleaner_sep)[0]
            print('\t'.join(entry))


# Parse command line options

def get_args():
    parser = ArgumentParser(
        description='Removes garbage from chromosome and gene IDs in a '
        'bed file.')
    parser.add_argument('input_bed', help='File to process', metavar='FILE.bed')
    parser.add_argument('--sep', '-s', help='Separator to remove text after')
    return parser.parse_args()


# Process file

def main(args):
    clean_bed(args.input_bed, args.sep)


if __name__ == '__main__':
    main(get_args())

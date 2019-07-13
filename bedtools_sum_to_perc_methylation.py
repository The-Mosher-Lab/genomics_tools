#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Convert the bed file summary of C and T calls per position to percent
# Created: 2019-07-12

from argparse import ArgumentParser


# Parse the bed file and calculate % methylation on the fly

def calc_methylation(input_file, mincov):
    with open(input_file, 'r') as input_handle:
        for line in input_handle:
            entry = line.strip().split()
            nC = int(entry[4])
            nT = int(entry[5])
            try:
                if (nC + nT) >= mincov:
                    perc_met = nC / (nC + nT) * 100
            except ZeroDivisionError:
                perc_met = 0
            print('\t'.join(entry[0:4]), perc_met, sep='\t')


# Get command line options

def get_args():
    parser = ArgumentParser(
        description='Calculate percent methylation from summed counts of '
        'methylated and unmethylated reads over a feature. Inteded for use with'
        ' the output of bedtools map, summing the C and T columns from '
        'MethylDackel\'s per-base output.')
    parser.add_argument('input_bed',
                        help='bed file to process with two score columns',
                        metavar='FILE.bed')
    parser.add_argument('-m', '--mincov',
                        help='Minimum coverage value to report methylation',
                        default=0)
    return parser.parse_args()


# Run

def main(args):
    calc_methylation(args.input_bed, args.mincov)


if __name__ == '__main__':
    main(get_args())

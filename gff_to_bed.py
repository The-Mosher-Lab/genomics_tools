#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Convert a gff3 to bed6 format for use with bedtools
# Created: 11/2017

from argparse import ArgumentParser


# Define function to parse and convert a gff3

def gff_to_bed(input_gff, gff_feature):
    score = '.'  # Score will be an unused column in the bed
    with open(input_gff, 'r') as input_handle:
        for line in input_handle:
            if not line == '\n' and not line.startswith('#'):
                entry = line.strip().split()
                if entry[2] == gff_feature:
                    chromosome = entry[0]
                    start = int(entry[3]) - 1  # 0-based
                    stop = int(entry[4])  # 1-based
                    feature_id = str(entry[8].split(';')[0])[3:]
                    strand = entry[6]
                    print(chromosome, start, stop, feature_id, score, strand, sep='\t')


# Parse command line options

def get_args():
    parser = ArgumentParser(
        description='Convert a gff3 to bed6 format for use with bedtools')
    parser.add_argument(
        'gff',
        help='A gff3 file to convert',
        metavar='FILE.gff3')
    parser.add_argument(
        '-f', '--feature',
        help='Features to extract from the gff3 file into bed format',
        metavar='FEATURE')
    return parser.parse_args()


# Convert the file

def main(args):
    gff_to_bed(args.gff, args.feature)


if __name__ == '__main__':
    gff_to_bed(get_args())

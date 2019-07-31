#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Convert a .bed file with 6 columns into a gtf format
# Created: 2019-04-19

from argparse import ArgumentParser


def bed_to_gtf(input_file, anno_source, feature_type):
    with open(input_file, 'r') as input_handle:
        for line in input_handle:
            entry = line.strip().split()
            chrom = entry[0]
            start = int(entry[1]) + 1  # To convert to 1-based coordinates
            stop = int(entry[2])
            name = entry[3]
            strand = entry[5]
            print(chrom, anno_source, feature_type, start, stop, '.', strand,
                  '.', 'gene_id "%s"; gene_name "%s"' % (name, name), sep='\t')


# Parse command line options

def get_args():
    parser = ArgumentParser(
        description='Coverts a 6 column .bed file int a gtf. Requires '
        'knowledge of the feature type and source fields. Very simple use-cases'
        'only.')
    parser.add_argument('input_bed',
                        help='File to process',
                        metavar='FILE.bed')
    parser.add_argument('--source', help='Source of the annotation', type=str)
    parser.add_argument('--feature',
                        help='The type of feature contained within the .bed file',
                        type=str)
    return parser.parse_args()


# Process the file

def main(args):
    bed_to_gtf(args.input_bed, args.source, args.feature)


if __name__ == '__main__':
    main(get_args())

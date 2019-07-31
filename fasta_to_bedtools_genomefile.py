#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Convert a .fasta file into a tab delimited that can be used with
# bedtools. With bedtools shuffle for example.
# Created: 11/2017

from argparse import ArgumentParser
from itertools import groupby


def convert_fasta(fasta_file, output_file):
    with open(fasta_file, 'r') as input_handle:
        for is_header, group in groupby(input_handle, lambda x: x.startswith('>')):
            if is_header:
                chromosome = next(group).strip('>').strip()
            else:
                seq_length = len(''.join(group).replace('\n', ''))
                print(chromosome, seq_length, sep='\t')


# Parse command line options

def get_args():
    parser = ArgumentParser(
        description='Convert a .fasta file into a tab delimited format that can'
        ' be used with bedtools')
    parser.add_argument(
        'fasta',
        help='An input fasta file containing all contigs',
        metavar='FILE.fasta')
    return parser.parse_args()


# Run the function to convert the file

def main(args):
    convert_fasta(args.fasta)


if __name__ == '__main__':
    main(get_args())

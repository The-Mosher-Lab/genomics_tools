#!/usr/bin/env python3

# Author: Jeffrey Grover
# Created: 11/2016
# Purpose: Calculate the n50 of a genome

from argparse import ArgumentParser
from itertools import groupby

# Functions


def get_chrom_lengths(genome_fasta):
    chrom_lengths = []
    with open(genome_fasta, 'r') as input_handle:
        fasta_reader = (
            x[1] for x in groupby(input_handle, lambda line: line.startswith('>')))
        for header in fasta_reader:
            next(header).strip('>').rstrip('\n')
            seq_length = len(''.join(s.strip() for s in next(fasta_reader)))
            chrom_lengths.append(seq_length)
    return chrom_lengths


def calc_n50(chrom_lengths):
    half_size = sum(chrom_lengths) / 2
    cumsum_chrom_lengths = 0
    for chrom_length in sorted(chrom_lengths, reverse=True):
        cumsum_chrom_lengths += chrom_length
        if cumsum_chrom_lengths >= half_size:
            return chrom_length


# Parse command line arguments

def get_args():
    parser = ArgumentParser(
        description='Calculate the n50 from a provided genome')
    parser.add_argument('input_fasta',
                        help='Input file to process',
                        metavar='.fasta')
    return parser.parse_args()


# Define a main function

def main(args):
    n50 = calc_n50(get_chrom_lengths(args.genome_fasta))
    print('N50: %s kb' % (n50 / 1000))


if __name__ == "__main__":
    main()

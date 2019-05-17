#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Pull sequence from a fasta file based on coordinates
# Created: 2019-05-17

from argparse import ArgumentParser
from itertools import groupby

# Functions


def fasta_iterate(fasta_file):
    with open(fasta_file, 'r') as reader:
        fasta_reader = (
            x[1] for x in groupby(reader, lambda line: line.startswith('>')))
        for header in fasta_reader:
            chromosome = next(header).strip('>').rstrip('\n')
            seq = ''.join(s.strip() for s in next(fasta_reader))
            yield (chromosome, seq)


def output_seq(fasta_iterator, search_chromosome, start, end):
    for chromosome, seq in fasta_iterator:
        if chromosome == search_chromosome:
            fasta_header = '>%s:%s-%s' % (chromosome, start, end)
            bases = seq[(start - 1):(end - 1)]
            print(fasta_header, bases, sep='\n')
            exit()


# Parse command line options

parser = ArgumentParser(
    description='Pull a sequence from a fasta file by coordinates.')
parser.add_argument(
    'fasta',
    help='An input fasta file to use as a reference',
    metavar='FILE')
parser.add_argument(
    '-c',
    '--chromosome',
    help='An input chromosome ID to search through',
    metavar='STRING')
parser.add_argument(
    '-s',
    '--start',
    help='Start position of the region to pull',
    type=int,
    metavar='INT')
parser.add_argument(
    '-n',
    '--end',
    help='End position of the region to pull',
    type=int,
    metavar='INT')

args = parser.parse_args()

# Process the file

output_seq(fasta_iterate(args.fasta), args.chromosome, args.start, args.end)

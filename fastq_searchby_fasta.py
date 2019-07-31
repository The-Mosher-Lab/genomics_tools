#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Search a .fastq file by entries in a .fasta
# Created: 02/2019

# This was created to search through small RNA fastq files for exact matches to
# a list of queries in .fasta format and output a list of counts.

import gzip
from argparse import ArgumentParser
from collections import OrderedDict


def magic_open(input_file):
    if input_file.endswith('gz'):
        return gzip.open(input_file, 'rt')
    else:
        return open(input_file, 'r')


def load_fasta(input_fasta):
    fasta_dict = OrderedDict()
    with magic_open(input_fasta) as input_handle:
        for line in input_handle:
            if line.startswith('>'):
                seq_ID = line[1:].split(' ')[0]
                sequence = next(input_handle).strip()
                fasta_dict[sequence] = {'id': seq_ID, 'count': 0}
    return fasta_dict


def search_fastq(input_fastq, search_dict):
    with magic_open(input_fastq) as input_handle:
        n = 0
        for line in input_handle:
            n += 1
            if n == 2 and line.strip() in search_dict:
                search_dict[line.strip()]['count'] += 1
            elif n == 4:
                n = 0
    return search_dict


def output_counts(input_dict, lib_name):
    print('ID', 'sequence', lib_name, sep=',')
    for sequence in input_dict:
        print(input_dict[sequence]['id'],
              sequence,
              input_dict[sequence]['count'],
              sep=',')


# Parse command line options

def get_args():
    parser = ArgumentParser(
        description='Reads a list of sequences in .fasta format and counts '
        'occurances of that sequence in a .fastq file.')
    parser.add_argument('-a', '--fasta',
                        help='Input .fasta, may be gzipped',
                        metavar='FILE.fasta(.gz)')
    parser.add_argument('-q', '--fastq',
                        help='Input .fastq, may be gzipped',
                        metavar='FILE.fastq(.gz)')
    parser.add_argument('-n', '--name',
                        help='Library ID or name',
                        metavar='String')
    return parser.parse_args()


# Parse and count

def main(args):
    output_counts(search_fastq(args.fastq, load_fasta(args.fasta)), args.name)


if __name__ == '__main__':
    main(get_args())

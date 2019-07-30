#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Reverse complement a fastq or fasta file
# per-base coverage output
# Created: 2019-07-29

from argparse import ArgumentParser
import gzip


# Functions

def magic_opener(input_file):
    if input_file.endswith('gz'):
        return gzip.open(input_file, 'rt')
    else:
        return open(input_file, 'r')


def fq_iter(input_file):
    n = 0
    fq_record = []
    with magic_opener(input_file) as input_handle:
        for line in input_handle:
            n += 1
            fq_record.append(line.strip())
            if n == 4:
                yield fq_record
                n = 0
                fq_record = []


def rev_comp(fq_iter):
    comp_table = str.maketrans('ATCG', 'TAGC')
    for record in fq_iter:
        seq_id = record[0]
        rev_comp_seq = record[1].translate(comp_table)[::-1]
        separator = record[2]
        qual = record[3][::-1]
        print(seq_id, rev_comp_seq, separator, qual, sep='\n')


# ArgumentParser

def get_args():
    parser = ArgumentParser(
        description='Returns the reverse complement of a fastq file to stdout.')
    parser.add_argument('fastq',
                        help='Input .fastq, may be gzipped',
                        metavar='FILE')
    return parser.parse_args()


# Entry point

def main(args):
    rev_comp(fq_iter(args.fastq))


if __name__ == '__main__':
    main(get_args())

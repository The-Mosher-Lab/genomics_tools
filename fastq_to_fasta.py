#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Filter .fastq reads between sizes defined by user input.
# Created: 12/2016

import re
import gzip
from argparse import ArgumentParser


def magic_open(input_file):
    if input_file.endswith('gz'):
        return gzip.open(input_file, 'rt')
    else:
        return open(input_file, 'r')


def fq_to_fa(input_fastq, output_path):
    n = 0
    fq_record = []
    with magic_open(input_fastq) as input_handle:
        for line in input_handle:
            n += 1
            fq_record.append(line.strip())
            if n == 4:
                fq_record[0] = re.sub(r'^@', '>', fq_record[0])
                print('\n'.join(fq_record[0, 1]))
                n = 0
                fq_record = []


# Parse command line options

def get_args():
    parser = ArgumentParser(
        description='Converts an input fastq file to fasta')
    parser.add_argument('fastq',
                        help='Input .fastq file, may be gzipped',
                        metavar='FILE.fastq(.gz)')
    return parser.parse_args()


# Convert the .fastq

def main(args):
    fq_to_fa(args.fastq)


if __name__ == '__main__':
    main(get_args())

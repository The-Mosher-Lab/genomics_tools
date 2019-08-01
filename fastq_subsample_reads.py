#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Randomly subsample reads from a fastq file
# Created: 2019-06-06

import random
import gzip
from argparse import ArgumentParser
from itertools import zip_longest
from sys import exit


def magic_open(input_file):
    if input_file.endswith('gz'):
        return gzip.open(input_file, 'rt')
    else:
        return open(input_file, 'r')


def get_total_fastq_records(input_fastq):
    with magic_open(input_fastq) as input_handle:
        fastq_lines = sum(1 for line in input_handle if line.strip())
        if fastq_lines % 4:
            exit('Error: Invalid fastq file, lines not divisible by 4.')
        else:
            return fastq_lines / 4


def num_records_from_percent(percent, total_fastq_records):
    return int((percent / 100) * total_fastq_records)


def get_random_record_indices(num_to_sample, total_fastq_records):
    return set(random.sample(range(total_fastq_records + 1), num_to_sample))


def read_fastq(input_fastq):
    with magic_open(input_fastq) as input_handle:
        fastq_iterator = (l.strip() for l in input_handle)
        for fastq_record in zip_longest(*[fastq_iterator] * 4):
            yield list(fastq_record)


def sample_fastq(fastq_reader, random_indices):
    record_num = 0
    for fastq_record in fastq_reader:
        record_num += 1
        if record_num in random_indices:
            print('\n'.join(fastq_record))


# Commandline parser

def get_args():
    parser = ArgumentParser(
        description='Randomly subsample a fastq file by either percent or total'
        ' number of reads')
    parser.add_argument('input_fastq',
                        help='Input file to process',
                        metavar='FILE')
    parser.add_argument('-r', '--reads',
                        help='Reads to sample',
                        type=int)
    parser.add_argument('-p', '--percent',
                        help='Percent of reads to sample (ex. 10)',
                        type=float)
    parser.add_argument('-s', '--seed',
                        help='Integer to use for a random seed',
                        default=None,
                        type=int)
    return parser.parse_args()


# Define a main function

def main(args):
    if not args.reads and not args.percent:
        exit('Error: You must supply a number of reads or percent to sample')
    elif args.reads and args.percent:
        exit('Error: You must supply only one of --reads or --percent')

    # Get total fastq records and validate

    num_fastq_records = get_total_fastq_records(args.input_fastq)

    # Get the random indices

    if args.percent:
        num_records = num_records_from_percent(args.percent, num_fastq_records)
    else:
        num_records = args.reads

    random.seed(args.seed)
    random_indices = get_random_record_indices(num_records, num_fastq_records)

    # Sample the fastq

    sample_fastq(read_fastq(args.input_fastq), random_indices)


if __name__ == "__main__":
    main(get_args())

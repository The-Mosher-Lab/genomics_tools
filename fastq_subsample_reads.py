#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Subsample .fastq reads
# Created: 5/2018

# Randomly subsets the reads from a fastq file based on user-defined parameters

import random
from sys import exit
from argparse import ArgumentParser

# Functions


def count_fastq_records(fastq_file):
    fastq_lines = 0
    with open(fastq_file) as input_handle:
        for line in input_handle:
            fastq_lines += 1
    fastq_records = int(fastq_lines / 4)
    return fastq_records


def random_fastq_indices(fastq_records, reads_to_sample):
    for i in range(reads_to_sample):
        random_indices = set(
            random.sample(range(fastq_records + 1), reads_to_sample))
    return random_indices


def subsample(fastq_file, fastq_records, random_indices, output_file):
    record_number = 0
    with open(fastq_file, 'r') as input_handle, open(output_file,
                                                     'w') as output_handle:
        for line1 in input_handle:
            line2 = next(input_handle)
            line3 = next(input_handle)
            line4 = next(input_handle)
            if record_number in random_indices:
                output_handle.write(line1)
                output_handle.write(line2)
                output_handle.write(line3)
                output_handle.write(line4)
            record_number += 1


# Parse command line options

parser = ArgumentParser(
    description='Subsample a specific number or percentage of reads from a '
    '.fastq file.')
parser.add_argument('input_file', help='Input .fastq file', metavar='File')
parser.add_argument(
    '-f', '--fraction', type=float, help='Fraction of reads to sample')
parser.add_argument(
    '-n', '--number', type=int, help='Number of reads to sample')

fastq_file = parser.parse_args().input_file
fraction = parser.parse_args().fraction
number = parser.parse_args().number

if fraction and number:
    exit('Specify either a number of reads or a percentage, not both.')

if not fraction and not number:
    exit('You must specify either a fraction or number of reads to sample.')

# Count fastq records

fastq_records = count_fastq_records(fastq_file)

# Determine reads to sample

if fraction:
    reads_to_sample = int(fastq_records * fraction)
else:
    reads_to_sample = number

# Create output file

output_file = fastq_file.split('.fastq')[0] + (
    '_' + str(reads_to_sample) + '.fastq')

# Generate random indices and output

random_indices = random_fastq_indices(fastq_records, reads_to_sample)
subsample(fastq_file, fastq_records, random_indices, output_file)

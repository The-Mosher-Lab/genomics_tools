#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Subsample .fastq reads
# Created: 5/2018

# Randomly subsets the reads from a fastq file based on user-defined parameters
# Only works on single-end reads until I feel like updating for PE reads

import random
import subprocess
import gzip
from sys import exit
from argparse import ArgumentParser

# Functions


def count_fastq_records(fastq_file, gzipped):  # wc -l is faster than python3
    if gzipped:
        fastq_lines = int(
            subprocess.getoutput('zcat ' + fastq_file + ' | wc -l').split()[0])
    else:
        fastq_lines = int(
            subprocess.getoutput('wc -l ' + fastq_file).split()[0])
    num_fastq_records = int(fastq_lines / 4)
    if fastq_lines % 4 == 0:
        return num_fastq_records
    else:
        exit('Invalid .fastq file. Lines not divisible by 4.')


def get_random_indices(num_fastq_records, reads_to_sample):
    for i in range(reads_to_sample):
        random_indices = set(
            random.sample(range(num_fastq_records + 1), reads_to_sample))
    return random_indices


def subsample(fastq_file, num_fastq_records, random_indices, output_file,
              gzipped):
    record_number = 0
    if gzipped:
        with gzip.open(fastq_file, 'rb') as input_handle, open(
                output_file, 'wb') as output_handle:
            for read_id in input_handle:
                record_number += 1
                if record_number in random_indices:
                    output_handle.write(read_id)
                    for i in range(3):
                        output_handle.write(
                            next(input_handle))  # Output record
                else:
                    for i in range(3):
                        next(input_handle)  # Skip record
    else:
        with open(fastq_file, 'r') as input_handle, open(output_file,
                                                         'w') as output_handle:
            for read_id in input_handle:
                record_number += 1
                if record_number in random_indices:
                    output_handle.write(read_id)
                    for i in range(3):
                        output_handle.write(
                            next(input_handle))  # Output record
                else:
                    for i in range(3):
                        next(input_handle)  # Skip record


# Parse command line options

parser = ArgumentParser(
    description='Subsample a specific number or percentage of reads from a '
    '.fastq file.')
parser.add_argument('input_file', help='Input .fastq file', metavar='File')
parser.add_argument(
    '-f', '--fraction', type=float, help='Fraction of reads to sample')
parser.add_argument(
    '-n', '--number', type=int, help='Number of reads to sample')
parser.add_argument(
    '-z',
    '--gzipped',
    action='store_true',
    help='Indicate whether your .fastq file is gzipped or not')

fastq_file = parser.parse_args().input_file
fraction = parser.parse_args().fraction
number = parser.parse_args().number
gzipped = parser.parse_args().gzipped

# Validate parameters for subsampling

if fraction and number:
    exit('Specify either a number of reads or a percentage, not both.')
if not fraction and not number:
    exit('You must specify either a fraction or number of reads to sample.')
if not fastq_file:
    exit('You must specify an input .fastq file.')

# Count fastq records

num_fastq_records = count_fastq_records(fastq_file, gzipped)

# Determine reads to sample

if fraction:
    reads_to_sample = int(num_fastq_records * fraction)
else:
    reads_to_sample = number

# Create output file

output_file = fastq_file.split('.fastq')[0] + (
    '_' + str(reads_to_sample) + '.fastq')

# Generate random indices and output

random_indices = get_random_indices(num_fastq_records, reads_to_sample)
subsample(fastq_file, num_fastq_records, random_indices, output_file, gzipped)

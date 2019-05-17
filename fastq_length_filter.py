#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Filter .fastq reads between sizes defined by user input.
# Created: 12/2016

from argparse import ArgumentParser


def filter_by_length(input_path, output_path, min_length, max_length):
    n = 0
    seq_list = []
    with open(input_path, 'r') as input_file, \
         open(output_path, 'w') as output_file:
        for line in input_file:
            n += 1
            seq_list.append(line)
            if n == 4:
                if min_length < len(seq_list[1]) <= (max_length + 1):
                    [output_file.write('%s' % item) for item in seq_list]
                n = 0
                seq_list = []


# Parse command line options

parser = ArgumentParser(
    description='Filters a given fastq file for reads between a supplied'
    'minimum and maximum length')
parser.add_argument('input_path', help='Input .fastq file', metavar='File')
parser.add_argument('--min', help='Minimum length for filtering', type=int)
parser.add_argument('--max', help='Maximum length for filtering', type=int)

input_fastq = parser.parse_args().input_path
min_fastq = parser.parse_args().min
max_fastq = parser.parse_args().max
output_fastq = input_fastq.rstrip('.fastq') + '.filtered_%s-%s.fastq' % (
    min_fastq, max_fastq)

# Filter the .fastq

filter_by_length(input_fastq, output_fastq, min_fastq, max_fastq)

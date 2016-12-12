#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Filter .fastq reads between sizes defined by user input.
# Created: 12/2016

# The first option is an input fastq file, --min and --max are min and max length to filter
# The output file will be another fastq with the length filtering appended to the filename
# Use find -exec to batch process: ex. 'find . -name "*.fastq" -exec "./fastq_length_filter.py" {} --min 25 --max 27 \;'

import re
from argparse import ArgumentParser


# Define function to iterate over fastq reads and output reads to new file if between min and max length


def filter_by_length(inpath, outpath, min_length, max_length):
    n = 0
    seq_list = []
    output_file = open(outpath, 'w')
    input_file = open(inpath, 'r')
    for line in input_file:
        n += 1
        seq_list.append(line)
        if n == 4:
            if min_length < len(seq_list[1]) <= (max_length + 1):  # Had to do it this way for some unknown reason
                [output_file.write('%s' % item) for item in seq_list]
            n = 0
            seq_list = []
    output_file.close()
    input_file.close()


# Parse command line options

parser = ArgumentParser(
    description='Filters a given fastq file for reads between a supplied minimum and maximum length')

parser.add_argument('input_path', help='Input .fastq file', metavar='File')

parser.add_argument('--min', help='Minimum length for filtering', type=int)

parser.add_argument('--max', help='Maximum length for filtering', type=int)

input_fastq = parser.parse_args().input_path
min_fastq = parser.parse_args().min
max_fastq = parser.parse_args().max
output_fastq = re.sub(r'\.fastq$', '.filtered_%s-%s.fastq' % (min_fastq, max_fastq), input_fastq)

# Filter the .fastq

filter_by_length(input_fastq, output_fastq, min_fastq, max_fastq)

#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Report SNPS, or more accurate "mismatches" in sam alignment
# Created: 2/2018

import csv
from argparse import ArgumentParser

# Function to parse a sam alignment


def parse_sam(input_sam):
    with open(input_sam, 'r') as input_handle:
        input_reader = csv.reader(input_handle, delimiter='\t')
        n_lines = 0
        total_mismatches = 0
        for line in input_reader:
            if not line[0].startswith('@'):  # Skip the header
                n_lines += 1
                for field in line:
                    if field.startswith('MD:Z:'):
                        md_field = field.strip('MD:Z:')
                        mismatches = sum(c.isalpha() for c in md_field)
                        total_mismatches = total_mismatches + mismatches
    mismatches_per_read = total_mismatches / n_lines
    print('Total Reads: ', n_lines)
    print('Total Mismatches: ', total_mismatches)
    print('Mismatches per Read: ', mismatches_per_read)


# Parse command line options

parser = ArgumentParser(description='Count mismatches in sam alignment.')
parser.add_argument('input_sam', help='.sam file to process', metavar='File')

input_sam = parser.parse_args().input_sam

# Process the file

parse_sam(input_sam)

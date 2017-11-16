#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Filter the combined "shortstack_full_report.csv" for loci expressed
# above a threshold in one sample. Outputs to stdout.
# Created: 7/2017

import csv
from argparse import ArgumentParser

# Define function to filter output loci for expression above a threshold


def filter_by_expression(input_report, threshold, test_column, control_column,
                         direction):
    with open(input_report, 'r') as input_handle:
        input_reader = csv.reader(input_handle)
        print(','.join(next(input_reader)))
        for row in input_reader:
            locus_expression = float(row[test_column])
            control_expression = float(row[control_column])
            if direction == 'above':
                if locus_expression >= threshold * control_expression:
                    print(','.join(row))
            elif direction == 'below':
                if locus_expression <= threshold * control_expression:
                    print(','.join(row))


# Parse command line options

parser = ArgumentParser(
    description='Filter the combined "shortstack_full_report.csv" for loci '
    'with expression at or above a threshold in one sample.')
parser.add_argument(
    '--threshold',
    help='Expression threshold to test (as a decimal).',
    type=float,
    metavar='FLOAT')
parser.add_argument(
    '--direction',
    choices=('above', 'below'),
    help='Direction to test expression vs control.')
parser.add_argument(
    '--testcolumn',
    help='The column in "shortstack_full_report.csv" for the sample to test.',
    type=int,
    metavar='INT')
parser.add_argument(
    '--control',
    help='The column in "shortstack_full_report.csv" for the control sample.',
    type=int,
    metavar='INT')
parser.add_argument(
    'input_path',
    help='Shortstack full report (.csv) to process.',
    metavar='File')

test_column = parser.parse_args().testcolumn - 1  # Humans count starting at 1
control_column = parser.parse_args().control - 1
threshold = parser.parse_args().threshold
input_path = parser.parse_args().input_path
direction = parser.parse_args().direction

# Process the file

filter_by_expression(input_path, threshold, test_column, control_column,
                     direction)

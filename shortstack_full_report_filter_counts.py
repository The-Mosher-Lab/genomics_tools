#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Filter the combined "shortstack_full_report.csv" for loci expressed above a threshold in one sample.
# Created: 7/2017

import csv
from argparse import ArgumentParser

# Define function to filter output loci for expression above a threshold in one sample


def filter_by_expression(input_report, threshold, column):
    with open(input_report, 'r') as input_handle:
        input_csv = csv.reader(input_handle)
        print(','.join(next(input_csv)))
        for row in input_csv:
            sample = int(row[column])
            if sample >= threshold:
                print(','.join(row))

# Parse command line options

parser = ArgumentParser(description='Filter the combined "shortstack_full_report.csv" for loci with expression at or '
                                    'above a threshold in one sample.')
parser.add_argument('-t', '--threshold', help='Expression threshold to test.', type=int)
parser.add_argument('-c', '--column', help='The column in "shortstack_full_report.csv" for the sample to test.',
                    type=int)
parser.add_argument('input_path', help='File to process', metavar='File')

library = parser.parse_args().column - 1  # Because humans count starting at 1 not 0
expression = parser.parse_args().threshold
input_path = parser.parse_args().input_path

# Process the file

filter_by_expression(input_path, expression, library)

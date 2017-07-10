#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: To determine which small RNA loci are present above an expression threshold in a sample and their expression
# Created: 7/2017

# Outputs the loci present above a threshold in one genotype and their expression levels.

import csv
from argparse import ArgumentParser


# Define function to parse the shortstack results file and output rows where expression of rdr2 is above a threshold

def get_loci(input_file, threshold):
    significance_threshold = 1 - (threshold / 100)
    with open(input_file, 'r') as input_handle:
        input_csv = csv.reader(input_handle, delimiter=',')
        print(', '.join(next(input_csv)))
        for row in input_csv:
            wt = float(row[3])
            rdr2 = float(row[6])
            if rdr2 <= wt * significance_threshold:
                print(', '.join(row))


# Parse command line options

parser = ArgumentParser(description='This outputs loci present above a threshold in one sample from shortstack results')
parser.add_argument('-s', '--significance', help='Percentage reduction to test', type=float)
parser.add_argument('input_path', help='Input file', metavar='File')

input_path = parser.parse_args().input_path
reduction_signifiance = parser.parse_args().significance

# Analyze the data

get_loci(input_path, reduction_signifiance)
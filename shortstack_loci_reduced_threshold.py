#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: To determine which small RNA loci are reduced below a threshold in a sequencing library of your choosing.
# Created: 7/2017

# This script will load in a .csv file containing small RNA loci expression where the first four columns are Locus,
# Name, Length, and WT. It accepts two command line arguments which is the column of the sequencing library to test
# vs WT, and the specified expression threshold.

# The script will output the results to stdout

from csv import reader
from argparse import ArgumentParser


# Define a function to iterate over the csv file to determine whether the expression is less than or equal to the
# supplied threshold in WT.

def reduction_test(input_file, reduction_threshold, column):
    column = column - 1   # Humans usually specify numbers beginning at 1
    with open(input_file, 'r') as input_handle:
        input_csv = reader(input_handle)
        print(', '.join(next(input_csv)))
        for row in input_csv:
            wt = float(row[3])
            test_library = float(row[column])
            if test_library <= wt * reduction_threshold:
                print(', '.join(row))


# Parse commandline options

parser = ArgumentParser(description='This outputs loci that are reduced below a threshold of wild-type expression in '
                                    'the sequencing library specified by column from shortstack combined results '
                                    'data. The file must contain Locus, Name, Size, and WT expression in the first '
                                    'four rows.')
parser.add_argument('-t', '--threshold', help='Expression threshold to compare vs WT', type=float)
parser.add_argument('-c', '--column', help='The column containing the expression data to test', type=int)
parser.add_argument('input_path', help='Input file', metavar='File')

input_path = parser.parse_args().input_path
threshold = parser.parse_args().threshold
sample = parser.parse_args().column

# Analyze the data

reduction_test(input_path, threshold, sample)

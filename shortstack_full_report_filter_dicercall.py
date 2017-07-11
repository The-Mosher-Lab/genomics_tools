#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Filter the combined "shortstack_full_report.csv" for loci of a defined small RNA size
# Created: 7/2017

import csv
from argparse import ArgumentParser


# Define function to filter output loci of a defined size class

def filter_by_dicercall(input_report, input_dicercall, output_results):
    with open(input_report, 'r') as input_handle:
        input_csv = csv.reader(input_handle)
        with open(output_results, 'w') as output_handle:
            output_csv = csv.writer(output_handle)
            output_csv.writerow(next(input_csv))
            for row in input_csv:
                dicercall = row[11]
                if dicercall == 'N':
                    dicercall = 0   # Kind of hacky, but next(dicercall) led to skipping lines after an 'N'
                if int(dicercall) == input_dicercall:
                    output_csv.writerow(row)

# Parse command line options

parser = ArgumentParser(description='Filter the combined "shortstack_full_report.csv" for loci of a defined small RNA '
                                    'size. This must be run in the same folder as a file titled '
                                    '"shortstack_full_report.csv."')
parser.add_argument('--size', help='Size class of loci to retrieve', type=int)

size_class = parser.parse_args().size
output_path = 'shortstack_full_report_%snt.csv' % size_class
input_path = './shortstack_full_report.csv'

# Filter the data

filter_by_dicercall(input_path, size_class, output_path)

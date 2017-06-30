#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Filter shortstack "Results.txt" output for loci of a defined size
# Created: 6/2017

# Filters shortstack results.txt loci of a size defined by user input

import csv
from argparse import ArgumentParser


# Define function to filter output loci of a defined size class

def filter_by_dicercall(input_results, input_dicercall, output_results):
    with open(input_results, 'r') as results:
        results_tsv = csv.reader(results, delimiter='\t')
        with open(output_results, 'w') as output_handle:
            output_csv = csv.writer(output_handle)
            output_csv.writerow(next(results_tsv))
            for row in results_tsv:
                dicercall = row[11]
                if dicercall == 'N':
                    dicercall = 0   # Kind of hacky, but next(dicercall) led to skipping lines after an 'N'
                if int(dicercall) == input_dicercall:
                    output_csv.writerow(row)

# Parse command line options

parser = ArgumentParser(description='Filter shortstack "Results.txt" output for loci of a defined size. Requires '
                                    'Results.txt from a shortstack run in the same folder.')
parser.add_argument('--size', help='Size class of loci to retrieve', type=int)

size_class = parser.parse_args().size
output_path = 'results_%snt.txt' % size_class
results_path = './Results.txt'

# Filter the data

filter_by_dicercall(results_path, size_class, output_path)

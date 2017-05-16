#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Filter shortstack "counts.txt" output for loci of a defined size
# Created: 5/2017

# Takes shortstack results.txt and counts.txt and filters counts.txt for loci of a size defined by user input

import csv
from argparse import ArgumentParser


# Define function to filter output loci of a defined size class

def filter_by_dicercall(input_results, input_counts, input_dicercall, output_counts):
    loci_list = []
    with open(input_results, 'r') as results:
        results_tsv = csv.reader(results, delimiter='\t')
        next(results_tsv)
        for row in results_tsv:
            locus = row[0]
            dicercall = row[11]
            if dicercall == 'N':
                dicercall = 0   # Kind of hacky, but next(dicercall) led to skipping lines after an 'N'
            if int(dicercall) == input_dicercall:
                loci_list.append(locus)
    with open(input_counts, 'r') as counts:
        counts_tsv = csv.reader(counts, delimiter='\t')
        with open(output_counts, 'w') as output_handle:
            output_csv = csv.writer(output_handle)
            output_csv.writerow(next(counts_tsv))
            for row in counts_tsv:
                locus = row[0]
                if locus in loci_list:
                    output_csv.writerow(row)


# Parse command line options

parser = ArgumentParser(description='Filters shortstack counts.txt for loci of a user-defined size class. Requires '
                                    'counts.txt and results.txt from a shortstack run in the same folder.')
parser.add_argument('--size', help='Size class of loci to retrieve', type=int)

size_class = parser.parse_args().size
output_path = 'counts_%snt.txt' % size_class
results_path = './Results.txt'
counts_path = './Counts.txt'

# Filter the data

filter_by_dicercall(results_path, counts_path, size_class, output_path)

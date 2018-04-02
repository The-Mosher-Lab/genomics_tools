#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Created to convert an annotated deseq2 results file to .bed format
# Created: 04/2018

import csv
from argparse import ArgumentParser

# Define functions


def deseq2bed(input_file):
    with open(input_file, 'r') as input_handle:
        results = csv.reader(input_handle)
        next(results)
        for row in results:
            chromosome = row[0]
            gene_id = row[1]
            start = row[3]
            stop = row[4]
            strand = row[5]
            print(chromosome, start, stop, gene_id, '.', strand, sep='\t')


# Parse command line options

parser = ArgumentParser(
    description='Converts an annotated DESeq2 results file to .bed format')
parser.add_argument('annotated_results', help='Input file', metavar='File')

input_file = parser.parse_args().annotated_results

# Run the function to convert the file

deseq2bed(input_file)

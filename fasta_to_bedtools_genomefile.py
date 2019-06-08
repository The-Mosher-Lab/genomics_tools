#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Convert a .fasta file into a tab delimited that can be used with
# bedtools. With bedtools shuffle for example.
# Created: 11/2017

import csv
from argparse import ArgumentParser
from itertools import groupby

# Parsing and overlap functions here


def convert_fasta(fasta_file, output_file):
    with open(fasta_file, 'r') as input_handle, open(output_file, 'w') as output_handle:
        output_writer = csv.writer(output_handle, delimiter='\t')
        for is_header, group in groupby(input_handle, lambda x: x.startswith('>')):
            if is_header:
                chromosome = next(group).strip('>').rstrip('\n')
            else:
                seq_length = len(''.join(group).replace('\n', ''))
                output_writer.writerow([chromosome, seq_length])


# Parse command line options

parser = ArgumentParser(
    description='Convert a .fasta file into a tab delimited format that can '
    'be used with bedtools')
parser.add_argument(
    'fasta_file',
    help='An input fasta file containing all contigs',
    metavar='FILE')

fasta_file = parser.parse_args().fasta_file
output_file = fasta_file.rsplit('.', 1)[0] + '.genome'

# Run the function to convert the file

convert_fasta(fasta_file, output_file)

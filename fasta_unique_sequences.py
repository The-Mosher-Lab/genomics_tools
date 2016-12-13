#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Read a .fasta file and output only unique sequences
# Created: 12/2016

# Extracts only the unique reads from a .fasta file
# Use find -exec to batch process: ex. 'find . -name "*.fasta" -exec "./fasta_unique_sequences.py" {} \;'

import re
from argparse import ArgumentParser
from itertools import groupby

# Define the function to check for unique sequences


def unique_seq(input_path, output_path):
    ishead = lambda x: x.startswith('>')  # fasta records all start with > in the header
    all_seqs = set()
    with open(input_path, 'r') as input_handle:
        with open(output_path, 'w') as output_handle:
            head = None
            for h, lines in groupby(input_handle, ishead):  # Group the input files by the header
                if h:
                    head = next(lines)
                else:
                    seq = ''.join(lines)
                    if seq not in all_seqs:  # Check whether the sequence is in the set of all_seqs
                        all_seqs.add(seq)
                        output_handle.write('%s%s' % (head, seq))

# Parse command line options

parser = ArgumentParser(
    description='Reads a .fasta file and outputs another .fasta with only unique sequences from the input file')
parser.add_argument('input_path', help='Input .fasta file', metavar='File')

input_fasta = parser.parse_args().input_path
output_fasta = re.sub(r'\.fasta$', '.unique.fasta', input_fasta)

# Parse the input.fasta and output unique sequences

unique_seq(input_fasta, output_fasta)

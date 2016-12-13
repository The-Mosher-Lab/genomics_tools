#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Filter .fastq reads between sizes defined by user input.
# Created: 12/2016

# Extracts reads from a .fastq file and creates a multiline fasta file from them
# Use find -exec to batch process: ex. 'find . -name "*.fastq" -exec "./fastq_to_fasta.py" {} \;'

import re
from argparse import ArgumentParser


# Define function to iterate over fastq reads and output reads to new file in fasta format


def fq_to_fa(input_path, output_path):
    n = 0
    fq_record = []
    with open(input_path, 'r') as input_file:
        with open(output_path, 'w') as output_file:
            for line in input_file:
                n += 1
                fq_record.append(line)
                if n == 4:
                    output_file.write(re.sub(r'^@', '>', fq_record[0]))
                    output_file.write(fq_record[1])
                    n = 0
                    fq_record = []


# Parse command line options

parser = ArgumentParser(description='Converts an input fastq file to fasta')
parser.add_argument('input_path', help='Input .fastq file', metavar='File')

input_fastq = parser.parse_args().input_path
output_fasta = re.sub(r'\.fastq$', '.fasta', input_fastq)

# Convert the .fastq

fq_to_fa(input_fastq, output_fasta)

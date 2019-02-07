#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Search a .fastq file by entries in a .fasta
# Created: 02/2019

# This was created to search through small RNA fastq files for exact matches to
# a list of queries in .fasta format and output a list of counts.

import re
from argparse import ArgumentParser

# Functions block


def load_fasta(input_fasta):
    fasta_seqs = {}
    with open(input_fasta, 'r') as input_handle:
        head = None
        for line in input_handle:
            if line.startswith('>'):
                seq_ID = line.split('>')[1].split(' ')[0]
            else:
                sequence = line.strip()
                fasta_seqs[sequence] = {'id': seq_ID, 'count': 0}
    return fasta_seqs


def search_fastq(input_fastq, search_dict):
    n = 0
    with open(input_fastq, 'r') as input_handle:
        for line in input_handle:
            if n == 1 and line.strip() in search_dict:
                search_dict[line.strip()]['count'] += 1
            elif n == 4:
                n = 0
            else:
                n += 1
    return search_dict


def output_counts(input_dict, lib_name):
    print('ID', 'sequence', lib_name, sep=',')
    for sequence in input_dict:
        print(
            input_dict[sequence]['id'], sequence, input_dict[sequence]['count'],
            sep=',')


# Parse command line options

parser = ArgumentParser(
    description=
    'Reads a list of sequences in .fasta format and counts occurances of that '
    'sequence in a .fastq file.')
parser.add_argument('--fa', help='Input .fasta', metavar='File')
parser.add_argument('--fq', help='Input .fastq', metavar='File')
parser.add_argument('-n', '--name', help='Library ID or name', metavar='String')

input_fasta = parser.parse_args().fa
input_fastq = parser.parse_args().fq
lib_name = parser.parse_args().name

# Parse and count

output_counts(search_fastq(input_fastq, load_fasta(input_fasta)), lib_name)

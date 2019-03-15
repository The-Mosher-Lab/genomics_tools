#!/usr/bin/env python3
# Author: Jeffrey Grover
# Purpose: Append a string to all chromosome IDs
# Created: 2019-03-14

# Define functions

from argparse import ArgumentParser


def append_chromosome(input_file, string):
    with open(input_file, 'r') as input_handle:
        for line in input_handle:
            entry = line.strip().split('\t')
            chrom = entry[0] + string
            source = entry[1]
            feature = entry[2]
            start = entry[3]
            stop = entry[4]
            score = entry[5]
            strand = entry[6]
            frame = entry[7]
            group = entry[8].split('; ')
            transcript_id = group[0]
            gene_id = group[1]
            gene_name = group[2]
            print(chrom, source, feature, start, stop, score, strand, frame,
                  sep='\t', end='\t')
            print(transcript_id, gene_id, gene_name, sep='; ')


# Parse command line options

parser = ArgumentParser(
    description='Appends a string to all chromosomes in a GTF file')
parser.add_argument('input_path', help='File to process', metavar='File')
parser.add_argument('--string', '-s', help='String to add to each chromosome ID')

input_path = parser.parse_args().input_path
string = parser.parse_args().string

# Process file

append_chromosome(input_path, string)

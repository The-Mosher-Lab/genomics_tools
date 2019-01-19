#!/usr/bin/env python3
# Author: Jeffrey Grover
# Purpose: Clean garbage from bed files in the chromosome ID fields
# Created: 09/2018

# Note, this was created in a hurry, and worked for the one use case I made it
# for. However, use at your own risk.

from argparse import ArgumentParser


def clean_bed(input_file, cleaner_sep):
    with open(input_file, 'r') as input_handle:
        for line in input_handle:
            entry = line.split('\t')
            chrom = entry[0].split(cleaner_sep)[0]
            start = entry[1]
            stop = entry[2]
            feature_id = entry[3]
            feature_family = entry[4]
            strand = entry[5].split('\n')[0]
            print(chrom, start, stop, feature_id, feature_family, strand,
                  sep='\t')


# Parse command line options

parser = ArgumentParser(
    description='Removes garbage from chromosome and gene IDs in a '
    'bed file. Works on at least the one file I needed it to.')
parser.add_argument('input_path', help='File to process', metavar='File')
parser.add_argument('--sep', '-s', help='Separator to remove text after')

input_path = parser.parse_args().input_path
cleaner_sep = parser.parse_args().sep

# Process file

clean_bed(input_path, cleaner_sep)

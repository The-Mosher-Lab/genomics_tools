#!/usr/bin/env python3
# Author: Jeffrey Grover
# Purpose: Clean garbage from gtf files in the chromosome ID and gene ID fields
# Created: 09/2018

# Note, this was created in a hurry, and worked for the one use case I made it
# for. However, use at your own risk. GTF/GFF format is notoriously nonstandard

from argparse import ArgumentParser


def clean_gtf(input_file, cleaner_sep):
    with open(input_file, 'r') as input_handle:
        for line in input_handle:
            entry = line.split('\t')
            chrom = entry[0].split(cleaner_sep)[0]
            source = entry[1]
            feature = entry[2]
            start = entry[3]
            stop = entry[4]
            score = entry[5]
            strand = entry[6]
            frame = entry[7]
            group = entry[8].split('; ')
            transcript_id = group[0].split(cleaner_sep)[0]
            gene_id = group[1].split(cleaner_sep)[0]
            gene_name = group[2].split(cleaner_sep)[0]
            print(chrom, source, feature, start, stop, score, strand, frame,
                  sep='\t', end='\t')
            print(transcript_id, gene_id, gene_name, sep='"; ', end='"\n')


# Parse command line options

parser = ArgumentParser(
    description='Removes garbage from chromosome and gene IDs in a '
    'gtf file. Works on at least the one file I needed it to')
parser.add_argument('input_path', help='File to process', metavar='File')
parser.add_argument('--sep', '-s', help='Separator to remove text after')

input_path = parser.parse_args().input_path
cleaner_sep = parser.parse_args().sep

# Process file

clean_gtf(input_path, cleaner_sep)

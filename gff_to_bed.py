#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Convert a gff3 to bed6 format for use with bedtools
# Created: 11/2017

import csv
from argparse import ArgumentParser

# Define function to parse and convert a gff3


def gff_to_bed(input_gff, gff_feature, output_bed):
    score = '.'  # Score will be an unused column in the bed
    with open(input_gff, 'r') as input_handle:
        input_reader = csv.reader(
            (line for line in input_handle if not line.startswith('#')),
            delimiter='\t')
        with open(output_bed, 'w') as output_handle:
            output_writer = csv.writer(output_handle, delimiter='\t')
            for line in input_reader:
                if line[2] == gff_feature:
                    chromosome = line[0]
                    start = int(line[3]) - 1  # 0-based
                    stop = int(line[4])  # 1-based
                    feature_id = str(line[8].split(';')[0])[3:]
                    strand = line[6]
                    bed_entry = [
                        chromosome, start, stop, feature_id, score, strand
                    ]
                    output_writer.writerow(bed_entry)


# Parse command line options

parser = ArgumentParser(
    description='Convert a gff3 to bed6 format for use with bedtools')
parser.add_argument(
    'input_gff',
    help='A gff3 file to convert',
    metavar='.gff3')
parser.add_argument(
    '-f', '--feature',
    help='Features to extract from the gff3 file into bed format',
    metavar='FEATURE')

input_gff = parser.parse_args().input_gff
gff_feature = parser.parse_args().feature
output_bed = input_gff.rsplit('.gff', 1)[0] + '_%s.bed' % gff_feature

# Convert the file

gff_to_bed(input_gff, gff_feature, output_bed)

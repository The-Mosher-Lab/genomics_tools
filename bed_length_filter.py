#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Filter .bed file entries for a minimum or maximum size
# Created: 11/2017

import csv
from argparse import ArgumentParser
from sys import exit


def filter_bed(input_bed, min_length, max_length, output_bed):
    with open(input_bed, 'r') as input_handle, open(output_bed, 'w') as output_handle:
        bed_reader = csv.reader(input_handle, delimiter='\t')
        bed_writer = csv.writer(output_handle, delimiter='\t')
        for row in bed_reader:
            feature_length = int(row[2]) - int(row[1])
            if min_length and max_length:
                if feature_length >= min_length and feature_length <= max_length:
                    bed_writer.writerow(row)
            elif min_length and not max_length:
                if feature_length >= min_length:
                    bed_writer.writerow(row)
            elif max_length and not min_length:
                if feature_length <= max_length:
                    bed_writer.writerow(row)
            else:
                exit('Error: You must supply a min or max value')


# Parse command line args

parser = ArgumentParser(
    description='Filter a bed file for features that are larger than minimum '
    'length and smaller than  a maximum length')
parser.add_argument('input_bed', help='Input .bed file', metavar='FILE')
parser.add_argument(
    '--min',
    help='Minimum feature size in nt, default=0',
    metavar='INT',
    type=int,
    default=None)
parser.add_argument(
    '--max',
    help='Maximum feature size in nt, default=1000',
    metavar='INT',
    type=int,
    default=None)

input_bed = parser.parse_args().input_bed
min_length = parser.parse_args().min
max_length = parser.parse_args().max
output_bed = input_bed.rstrip('.bed') + '_min%s_max%s.bed' % (min_length,
                                                              max_length)

# Run the functions to output the new bed file

filter_bed(input_bed, min_length, max_length, output_bed)

#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Annotate deseq2 results with information from a bed file.
# Originally made to annotate TEs in a deseq2 results file with family info
# Created: 12/2017

import csv
from argparse import ArgumentParser

# Define functions


def parse_deseq2(input_file):
    deseq2_dict = {}
    with open(input_file, 'r') as input_handle:
        results = csv.reader(input_handle)
        next(results)
        for row in results:
            feature_id = row[0]
            remaining_fields = row[1:]
            deseq2_dict[feature_id] = [remaining_fields]
    return deseq2_dict


def get_header(input_file):
    with open(input_file, 'r') as input_handle:
        results = csv.reader(input_handle)
        header = next(results)
        header.insert(1, 'family')
    return header


def parse_bed(input_bed):
    bed_dict = {}
    with open(input_bed, 'r') as input_handle:
        bed = csv.reader(input_handle, delimiter='\t')
        for row in bed:
            feature_id = row[3]
            family = row[4]
            bed_dict[feature_id] = family
    return bed_dict


def annotate_deseq2(deseq2_dict, header, bed_dict, output_file):
    with open(output_file, 'w') as output_handle:
        annotated_results = csv.writer(output_handle)
        annotated_results.writerow(header)
        for feature_id in deseq2_dict:
            deseq2_info = deseq2_dict[feature_id][0]
            family = bed_dict[feature_id]
            output_row = [feature_id, family] + deseq2_info
            annotated_results.writerow(output_row)


# Parse command line options

parser = ArgumentParser(
    description='Annotate deseq2 results with TE family information from a bed')
parser.add_argument('--bed', help='Input bed file', metavar='File')
parser.add_argument('--deseq', help='Input deseq results', metavar='File')

bed_file = parser.parse_args().bed
deseq2_file = parser.parse_args().deseq
output_file = deseq2_file.rsplit('.')[0] + '_annotated.csv'

# Run the functions to create dictionaries

deseq2_result = parse_deseq2(deseq2_file)
header = get_header(deseq2_file)
bed = parse_bed(bed_file)

# Run the function to annotate the file

annotate_deseq2(deseq2_result, header, bed, output_file)

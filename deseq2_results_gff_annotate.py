#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Annotate the differentially expressed genes from DESeq2 with
# start/stop and feature information from a gff3. This will also work with any
# gene list where geneID is in the first column of a tsv/csv
# Created: 10/2017

import csv
from argparse import ArgumentParser

# Function definitions go here


def parse_deseq2(input_file, file_dialect):
    features_dict = {}
    with open(input_file, 'r') as input_handle:
        if file_dialect == 'csv':
            results = csv.reader(input_handle)
        elif file_dialect == 'tsv':
            results = csv.reader(input_handle, delimiter='\t')
        field_names = next(results)
        for row in results:
            feature_id = row[0]
            remaining_fields = row[1:]
            features_dict[feature_id] = [remaining_fields]
    return [features_dict, field_names]


def parse_gff(input_gff, gff_feature):
    gff_dict = {}
    with open(input_gff, 'r') as input_handle:
        gff3 = csv.reader(
            (row for row in input_handle if not row.startswith('#')),
            delimiter='\t')
        for row in gff3:
            if row[2] == gff_feature:
                chromosome = row[0]
                feature = row[2]
                start = int(row[3])
                stop = int(row[4])
                strand = row[6]
                feature_id = int(''.join(filter(str.isdigit, str(row[8].split(';')[0])[3:])))
                if chromosome not in gff_dict:
                    gff_dict[chromosome] = {}
                if feature_id not in gff_dict[chromosome]:
                    gff_dict[chromosome][feature_id] = {}
                gff_dict[chromosome][feature_id] = [
                    feature, start, stop, strand
                ]
        return gff_dict


def annotate_results(features_dict, gff3_dict, output_file, header):
    with open(output_file, 'w') as output_handle:
        output_file = csv.writer(output_handle)
        output_file.writerow(header)
        for feature in features_dict:
            feature_digits = int(''.join(filter(str.isdigit, feature)))
            for chromosome in gff3_dict:
                if feature_digits in gff3_dict[chromosome]:
                    feature_type = gff3_dict[chromosome][feature_digits][0]
                    start = gff3_dict[chromosome][feature_digits][1]
                    stop = gff3_dict[chromosome][feature_digits][2]
                    strand = gff3_dict[chromosome][feature_digits][3]
                    deseq2_info = features_dict[feature][0]
                    output_row = [
                        chromosome, feature, feature_type, start, stop, strand
                    ] + deseq2_info
                    output_file.writerow(output_row)


# Parse command line options

parser = ArgumentParser(
    description='Annotate the differentially expressed genes from DESeq2 with '
    'start/stop and feature information from a gff3. This will also work with '
    'any gene/feature list where geneID is in the first column of a tsv/csv')
parser.add_argument('--gff', help='Input gff3 file', metavar='File')
parser.add_argument('--deseq', help='Input ShortStack Report', metavar='File')
parser.add_argument('-d', '--deseq_dialect', help='tsv or csv')
parser.add_argument('-f', '--feature', help='String matching a gff feature')

gff_file = parser.parse_args().gff
deseq2_file = parser.parse_args().deseq
deseq2_dialect = parser.parse_args().deseq_dialect
feature = parser.parse_args().feature
output_file = deseq2_file.rsplit('.')[0] + '_annotated.csv'

# Run the functions to create dictionaries

deseq2_result = parse_deseq2(deseq2_file, deseq2_dialect)
deseq2_dict = deseq2_result[0]
deseq2_header = deseq2_result[1]
gff3_dict = parse_gff(gff_file, feature)

# Create the header for the output file

output_header = [
    'chromosome', 'feature_id', 'type', 'start', 'stop', 'strand'
] + deseq2_result[1][1:]

# Run the function to annotate the file

annotate_results(deseq2_dict, gff3_dict, output_file, output_header)

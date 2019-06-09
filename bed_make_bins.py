#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Create a new bed file where entries made of bins from the original
# This is most useful for creating metaplots or looking at expression over a
# fraction of the original features
# Created: 1/2018

import csv
from argparse import ArgumentParser


def parse_bed(input_bed):
    bed_dict = {}
    with open(input_bed, 'r') as input_handle:
        bed_file = csv.reader(input_handle, delimiter='\t')
        for line in bed_file:
            feature_id = line[3]
            bed_dict[feature_id] = {
                'chromosome': line[0],
                'start': int(line[1]),
                'stop': int(line[2]),
                'score': line[4],
                'strand': line[5]
            }
    return bed_dict


def create_bins(bed_dict, window_size, bin_width, output_prefix):
    num_bins = int(window_size / bin_width)
    for i in range(num_bins):
        bin_number = i + 1  # Humans count starting at 1

# Create the upstream bins

        upstream_file = output_prefix + 'u_' + str(bin_number).zfill(2) + '.bed'
        with open(upstream_file, 'w') as upstream_handle:
            upstream_writer = csv.writer(upstream_handle, delimiter='\t')
            for feature_id in bed_dict:
                chromosome = bed_dict[feature_id]['chromosome']
                if bed_dict[feature_id]['strand'] == '+':
                    start = bed_dict[feature_id]['start'] - (window_size - (bin_width * i))
                    stop = start + (bin_width - 1)
                elif bed_dict[feature_id]['strand'] == '-':
                    stop = bed_dict[feature_id]['stop'] + (window_size - (bin_width * i))
                    start = stop - (bin_width - 1)
                score = bed_dict[feature_id]['score']
                strand = bed_dict[feature_id]['strand']
                output_row = [chromosome, start, stop, feature_id, score, strand]
                if start >= 0 and stop >= 0:
                    upstream_writer.writerow(output_row)

# Create the downstream bins

        downstream_file = output_prefix + 'd_' + str(bin_number).zfill(2) + '.bed'
        with open(downstream_file, 'w') as downstream_handle:
            downstream_writer = csv.writer(downstream_handle, delimiter='\t')
            for feature_id in bed_dict:
                chromosome = bed_dict[feature_id]['chromosome']
                if bed_dict[feature_id]['strand'] == '+':
                    start = bed_dict[feature_id]['stop'] + ((bin_width * i) + 1)
                    stop = start + (bin_width - 1)
                elif bed_dict[feature_id]['strand'] == '-':
                    stop = bed_dict[feature_id]['start'] - ((bin_width * i) + 1)
                    start = stop - (bin_width - 1)
                score = bed_dict[feature_id]['score']
                strand = bed_dict[feature_id]['strand']
                output_row = [chromosome, start, stop, feature_id, score, strand]
                if start >= 0 and stop >= 0:
                    downstream_writer.writerow(output_row)

# Create the feature body bins

        body_file = output_prefix + 'b_' + str(bin_number).zfill(2) + '.bed'
        with open(body_file, 'w') as body_handle:
            body_writer = csv.writer(body_handle, delimiter='\t')
            for feature_id in bed_dict:
                chromosome = bed_dict[feature_id]['chromosome']
                feature_length = bed_dict[feature_id]['stop'] - bed_dict[feature_id]['start']
                body_bin_width = (feature_length / num_bins)
                if bed_dict[feature_id]['strand'] == '+':
                    start = int(round((bed_dict[feature_id]['start'] + (body_bin_width * i)), 0))
                    if i < (num_bins - 1):
                        stop = int(round((start + body_bin_width), 0) - 1)
                    elif i == (num_bins - 1):
                        stop = bed_dict[feature_id]['stop']
                elif bed_dict[feature_id]['strand'] == '-':
                    if i == 0:
                        stop = int(round((bed_dict[feature_id]['stop'] - (body_bin_width * i)), 0))
                    else:
                        stop = int(round((bed_dict[feature_id]['stop'] - (body_bin_width * i)), 0) - 1)
                    if i < (num_bins - 1):
                        start = int(round((stop - body_bin_width), 0))
                    elif i == (num_bins - 1):
                        start = bed_dict[feature_id]['start']
                score = bed_dict[feature_id]['score']
                strand = bed_dict[feature_id]['strand']
                output_row = [chromosome, start, stop, feature_id, score, strand]
                if start >= 0 and stop >= 0:
                    body_writer.writerow(output_row)


# Parse command line options

parser = ArgumentParser(
    description='Create separate bed files for desired bin sizes up and '
    'downstream of an input bed file. Divides feature bodies into an equal '
    'number of bins as well. Be sure to use bin widths that can be divided '
    'evenly into your window size or it will likely fail')
parser.add_argument('input_bed', help='bed file to process', metavar='File')
parser.add_argument('-w', '--window', help='Window size', type=int, metavar='Integer')
parser.add_argument('-b', '--bin_width', help='Bin size', type=int, metavar='Integer')
parser.add_argument('-o', '--output_prefix', help='Prefix for output files', metavar='File')

input_bed = parser.parse_args().input_bed
window_size = parser.parse_args().window
bin_width = parser.parse_args().bin_width
output_prefix = parser.parse_args().output_prefix

# Run the functions, create the bins

bed_dict = parse_bed(input_bed)
create_bins(bed_dict, window_size, bin_width, output_prefix)

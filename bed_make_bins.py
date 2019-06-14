#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Create a new bed file where entries made of bins from the original
# This is most useful for creating metaplots or looking at expression over a
# fraction of the original features
# Created: 2018-01-15
# Refactored: 2019-06-14

import csv
from argparse import ArgumentParser

# Subroutine functions


def parse_bed_to_dict(input_bed):
    bed_dict = {}
    with open(input_bed, 'r') as input_handle:
        for line in input_handle:
            entry = line.strip().split('\t')
            feature_id = entry[3]
            try:
                score = entry[4]
            except IndexError:
                score = '.'
            try:
                strand = entry[5]
            except IndexError:
                strand = '.'
            bed_dict[feature_id] = {
                'chromosome': entry[0],
                'start': int(entry[1]),
                'stop': int(entry[2]),
                'score': score,
                'strand': strand
            }
    return bed_dict


def create_upstream_bins(bed_dict, window_size, bin_width, output_prefix):
    num_bins = int(window_size / bin_width)
    for i in range(num_bins):
        bin_number = i + 1  # Humans count starting at 1
        upstream_file = '%su_%s.bed' % (output_prefix, str(bin_number).zfill(2))
        with open(upstream_file, 'w') as upstream_handle:
            upstream_writer = csv.writer(upstream_handle, delimiter='\t')
            for feature_id in bed_dict:
                chromosome = bed_dict[feature_id]['chromosome']
                score = bed_dict[feature_id]['score']
                strand = bed_dict[feature_id]['strand']
                if bed_dict[feature_id]['strand'] in ('+', '.'):
                    start = bed_dict[feature_id]['start'] - (window_size - (bin_width * i))
                    stop = start + (bin_width - 1)
                elif bed_dict[feature_id]['strand'] == '-':
                    stop = bed_dict[feature_id]['stop'] + (window_size - (bin_width * i))
                    start = stop - (bin_width - 1)
                output_row = [chromosome, start, stop, feature_id, score, strand]
                if start >= 0 and stop >= 0:
                    upstream_writer.writerow(output_row)


def create_downstream_bins(bed_dict, window_size, bin_width, output_prefix):
    num_bins = int(window_size / bin_width)
    for i in range(num_bins):
        bin_number = i + 1
        downstream_file = '%sd_%s.bed' % (output_prefix, str(bin_number).zfill(2))
        with open(downstream_file, 'w') as downstream_handle:
            downstream_writer = csv.writer(downstream_handle, delimiter='\t')
            for feature_id in bed_dict:
                chromosome = bed_dict[feature_id]['chromosome']
                score = bed_dict[feature_id]['score']
                strand = bed_dict[feature_id]['strand']
                if bed_dict[feature_id]['strand'] in ('+', '.'):
                    start = bed_dict[feature_id]['stop'] + ((bin_width * i) + 1)
                    stop = start + (bin_width - 1)
                elif bed_dict[feature_id]['strand'] == '-':
                    stop = bed_dict[feature_id]['start'] - ((bin_width * i) + 1)
                    start = stop - (bin_width - 1)
                output_row = [chromosome, start, stop, feature_id, score, strand]
                if start >= 0 and stop >= 0:
                    downstream_writer.writerow(output_row)


def create_body_bins(bed_dict, window_size, bin_width, output_prefix):
    num_bins = int(window_size / bin_width)
    for i in range(num_bins):
        bin_number = i + 1
        body_file = '%sb_%s.bed' % (output_prefix, str(bin_number).zfill(2))
        with open(body_file, 'w') as body_handle:
            body_writer = csv.writer(body_handle, delimiter='\t')
            for feature_id in bed_dict:
                chromosome = bed_dict[feature_id]['chromosome']
                score = bed_dict[feature_id]['score']
                strand = bed_dict[feature_id]['strand']
                feature_length = bed_dict[feature_id]['stop'] - bed_dict[feature_id]['start']
                body_bin_width = (feature_length / num_bins)
                if bed_dict[feature_id]['strand'] in ('+', '.'):
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
                output_row = [chromosome, start, stop, feature_id, score, strand]
                if start >= 0 and stop >= 0:
                    body_writer.writerow(output_row)


# Parse command line options

def get_args():
    parser = ArgumentParser(
        description='Create separate bed files for desired bin sizes up and '
        'downstream of an input bed file. Divides feature bodies into an equal '
        'number of bins as well. Be sure to use bin widths that can be divided '
        'evenly into your window size or it will likely fail.')
    parser.add_argument('input_bed',
                        help='bed file to process',
                        metavar='File.bed')
    parser.add_argument('-w', '--window',
                        help='Size of up and downstream windows (nt)',
                        type=int,
                        metavar='Integer')
    parser.add_argument('-b', '--bin_width',
                        help='Bin size (nt)',
                        type=int,
                        metavar='Integer')
    parser.add_argument('-o', '--output_prefix',
                        help='Prefix for output files',
                        metavar='Prefix[body, up, down]_bin#.bed')
    return parser.parse_args()


# Run the functions, create the bins

def main(args):
    bed_dict = parse_bed_to_dict(args.input_bed)
    create_body_bins(bed_dict, args.window, args.bin_width, args.output_prefix)
    create_upstream_bins(bed_dict, args.window, args.bin_width, args.output_prefix)
    create_downstream_bins(bed_dict, args.window, args.bin_width, args.output_prefix)


if __name__ == '__main__':
    args = get_args()
    main(args)

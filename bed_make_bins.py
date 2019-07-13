#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Create a new bed file where entries made of bins from the original
# This is most useful for creating metaplots or looking at expression over a
# fraction of the original features
# Created: 2018-01-15
# Refactored: 2019-06-22

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
        bin_start = window_size - (bin_width * i)
        bin_stop = bin_start - (bin_width - 1)
        upstream_file = '%su_%s_%s-%s.bed' % (output_prefix, str(bin_number).zfill(2), bin_start, bin_stop)
        with open(upstream_file, 'w') as upstream_handle:
            upstream_writer = csv.writer(upstream_handle, delimiter='\t')
            for feature_id in bed_dict:
                chromosome = bed_dict[feature_id]['chromosome']
                score = bed_dict[feature_id]['score']
                strand = bed_dict[feature_id]['strand']
                start = bed_dict[feature_id]['start']
                stop = bed_dict[feature_id]['stop']

                # Bins for + and unstranded start at the feature - window size

                if strand in ('+', '.'):
                    start = start - (window_size - (bin_width * i))
                    stop = start + (bin_width - 1)

                # Bins for - strand start at 1 beyond the stop

                elif strand == '-':
                    stop = stop + (window_size - (bin_width * i))
                    start = stop - (bin_width - 1)

                # Output bins, but only if the bins are valid coordinates

                if start >= 0 and stop >= 0:
                    output_row = [chromosome, start, stop, feature_id, score, strand]
                    upstream_writer.writerow(output_row)


def create_downstream_bins(bed_dict, window_size, bin_width, output_prefix):
    num_bins = int(window_size / bin_width)
    for i in range(num_bins):
        bin_number = i + 1
        bin_start = (bin_width * i) + 1
        bin_stop = (bin_start - 1) + bin_width
        downstream_file = '%sd_%s_%s-%s.bed' % (output_prefix, str(bin_number).zfill(2), bin_start, bin_stop)
        with open(downstream_file, 'w') as downstream_handle:
            downstream_writer = csv.writer(downstream_handle, delimiter='\t')
            for feature_id in bed_dict:
                chromosome = bed_dict[feature_id]['chromosome']
                score = bed_dict[feature_id]['score']
                strand = bed_dict[feature_id]['strand']
                start = bed_dict[feature_id]['start']
                stop = bed_dict[feature_id]['stop']

                # Bins for + and unstranded start at 1 beyond the feature stop

                if strand in ('+', '.'):
                    start = stop + ((bin_width * i) + 1)
                    stop = start + (bin_width - 1)

                # Bins for - strand start 1 before the start

                elif strand == '-':
                    stop = start - ((bin_width * i) + 1)
                    start = stop - (bin_width - 1)

                # Output bins, but only if the bins are valid coordinates

                if start >= 0 and stop >= 0:
                    output_row = [chromosome, start, stop, feature_id, score, strand]
                    downstream_writer.writerow(output_row)


def create_body_bins(bed_dict, window_size, bin_width, output_prefix):
    num_bins = int(window_size / bin_width)
    for i in range(num_bins):
        bin_number = i + 1
        bin_perc_length = bin_number * (100 / num_bins)
        body_file = '%sb_%s_%s.bed' % (output_prefix, str(bin_number).zfill(2), bin_perc_length)
        with open(body_file, 'w') as body_handle:
            body_writer = csv.writer(body_handle, delimiter='\t')
            for feature_id in bed_dict:
                chromosome = bed_dict[feature_id]['chromosome']
                score = bed_dict[feature_id]['score']
                strand = bed_dict[feature_id]['strand']
                start = bed_dict[feature_id]['start']
                stop = bed_dict[feature_id]['stop']
                feature_length = stop - start
                body_bin_width = (feature_length / num_bins)

                # For + strand or unstranded bin coordinates start at start + 1
                # First and last will be 1nt shorter to so exact start can be its own bin

                if strand in ('+', '.'):
                    if i == 0:
                        start = start + 1
                    else:
                        start = int(round((start + (body_bin_width * i)), 0))
                    stop = int(round((start + body_bin_width), 0) - 1)

                # For - strand bins are numbered from the bed file's "stop"
                # First will be 1nt shorter to so exact stop can be its own bin

                elif strand == '-':
                    if i == 0:
                        stop = int(round((stop - (body_bin_width * i)), 0) - 2)
                    else:
                        stop = int(round((stop - (body_bin_width * i)), 0) - 1)
                    start = int(round((stop - body_bin_width), 0))

                # Output bins, but only if the bins are valid coordinates

                if start >= 0 and stop >= 0:
                    output_row = [chromosome, start, stop, feature_id, score, strand]
                    body_writer.writerow(output_row)


def get_start_coords(bed_dict, output_prefix):
    start_file = '%sstart.bed' % output_prefix
    with open(start_file, 'w') as start_handle:
        start_writer = csv.writer(start_handle, delimiter='\t')
        for feature_id in bed_dict:
            chromosome = bed_dict[feature_id]['chromosome']
            score = bed_dict[feature_id]['score']
            strand = bed_dict[feature_id]['strand']
            start = bed_dict[feature_id]['start']
            stop = bed_dict[feature_id]['stop']

            # Start coordinates are zero-based already for + or unstranded

            if strand in ('+', '.'):
                stop = start + 1

            # For - strand some extra work is required

            elif strand == '-':
                start = stop - 1

            # Output bins

            output_row = [chromosome, start, stop, feature_id, score, strand]
            start_writer.writerow(output_row)


def get_stop_coords(bed_dict, output_prefix):
    stop_file = '%sstop.bed' % output_prefix
    with open(stop_file, 'w') as stop_handle:
        stop_writer = csv.writer(stop_handle, delimiter='\t')
        for feature_id in bed_dict:
            chromosome = bed_dict[feature_id]['chromosome']
            score = bed_dict[feature_id]['score']
            strand = bed_dict[feature_id]['strand']
            start = bed_dict[feature_id]['start']
            stop = bed_dict[feature_id]['stop']

            # Stop coordinate begins at stop -1 for + or unstranded

            if strand in ('+', '.'):
                start = stop - 1

            # Already zero baed for - strand

            elif strand == '-':
                stop = start + 1

            # Output bins

            output_row = [chromosome, start, stop, feature_id, score, strand]
            stop_writer.writerow(output_row)


# Parse command line options

def get_args():
    parser = ArgumentParser(
        description='Create separate bed files for desired bin sizes up and '
        'downstream of an input bed file. Divides feature bodies into an equal '
        'number of bins as well. Be sure to use bin widths that can be divided '
        'evenly into your window size or it will likely fail. Start and stop of'
        ' each feature is also output as a bin of length 1.')
    parser.add_argument('input_bed',
                        help='bed file to process',
                        metavar='FILE.bed')
    parser.add_argument('-w', '--window',
                        help='Size of up and downstream windows (nt)',
                        type=int,
                        metavar='INT')
    parser.add_argument('-b', '--bin_width',
                        help='Bin size (nt)',
                        type=int,
                        metavar='INT')
    parser.add_argument('-p', '--prefix',
                        help='Prefix for output files. Files will be output as: Prefix[body|up|down]_bin#_length[start-stop|percent].bed',
                        metavar='PREFIX')
    return parser.parse_args()


# Run the functions, create the bins

def main(args):
    bed_dict = parse_bed_to_dict(args.input_bed)
    create_body_bins(bed_dict, args.window, args.bin_width, args.output_prefix)
    create_upstream_bins(bed_dict, args.window, args.bin_width, args.output_prefix)
    create_downstream_bins(bed_dict, args.window, args.bin_width, args.output_prefix)
    get_start_coords(bed_dict, args.output_prefix)
    get_stop_coords(bed_dict, args.output_prefix)


if __name__ == '__main__':
    args = get_args()
    main(args)

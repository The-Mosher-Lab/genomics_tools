#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Find small RNA clusters from a ShortStack "full report" file that
# overlap with features in a gff3
# Created: 10/2017

import csv
from argparse import ArgumentParser

# Parsing and overlap functions here


def parse_gff(input_gff, gff_feature):
    gff_dict = {}
    with open(input_gff, 'r') as input_handle:
        input_file = csv.reader(
            (row for row in input_handle if not row.startswith('#')),
            delimiter='\t')
        for row in input_file:
            if row[2] == gff_feature:
                chromosome = row[0]
                feature = row[2]
                start = int(row[3])
                stop = int(row[4])
                strand = row[6]
                feature_id = str(row[8].split(';')[0])[3:]
                if chromosome not in gff_dict:
                    gff_dict[chromosome] = {}
                if feature_id not in gff_dict[chromosome]:
                    gff_dict[chromosome][feature_id] = {}
                gff_dict[chromosome][feature_id] = [
                    feature, start, stop, strand
                ]
        return gff_dict


def parse_shortstack_full_report(input_report):
    shortstack_dict = {}
    with open(input_report, 'r') as input_handle:
        input_reader = csv.reader(input_handle)
        next(input_reader)
        for row in input_reader:
            chromosome = row[0].split(':')[0]
            cluster_start = int(row[0].split(':')[1].split('-')[0])
            cluster_stop = int(row[0].split(':')[1].split('-')[1])
            cluster_name = row[1]
            shortstack_info = row[2:]
            if chromosome not in shortstack_dict:
                shortstack_dict[chromosome] = {}
            if cluster_name not in shortstack_dict[chromosome]:
                shortstack_dict[chromosome][cluster_name] = [
                    cluster_start, cluster_stop
                ] + shortstack_info
    return shortstack_dict


def overlap_shortstack_gff3(gff_dict, shortstack_dict, upstream_bp,
                            feature_body, downstream_bp, output_file):
    overlap_header = ['upstream', 'body', 'downstream']
    upstream_overlaps = 0
    downstream_overlaps = 0
    body_overlaps = 0
    with open(output_file, 'w') as output_handle:
        output_writer = csv.writer(output_handle)
        output_writer.writerow(overlap_header)
        for chromosome in gff_dict:
            if chromosome in shortstack_dict:
                for feature in gff_dict[chromosome]:
                    feature_start = gff_dict[chromosome][feature][1]
                    feature_stop = gff_dict[chromosome][feature][2]
                    for cluster in shortstack_dict[chromosome]:
                        cluster_start = shortstack_dict[chromosome][cluster][0]
                        if upstream_bp > 0 and feature_start - upstream_bp <= cluster_start <= feature_start:
                            upstream_overlaps += 1
                        if feature_body and feature_start <= cluster_start <= feature_stop:
                            body_overlaps += 1
                        if downstream_bp > 0 and feature_stop + downstream_bp >= cluster_start >= feature_stop:
                            downstream_overlaps += 1
        overlaps = [upstream_overlaps, body_overlaps, downstream_overlaps]
        print(overlap_header)
        print(overlaps)
        output_writer.writerow(overlaps)


# Parse command line options

parser = ArgumentParser(
    description='Looks for overlap between features of interest in a gff3 file'
    ' and siRNA clusters from a ShortStack full_report')
parser.add_argument(
    '--gff', help='Input gff3 file', metavar='File')
parser.add_argument(
    '--ssreport', help='Input ShortStack Report', metavar='File')
parser.add_argument(
    '--feature',
    help='Feature to look for overlap with from gff3 file',
    type=str)
parser.add_argument(
    '--upstream',
    help='Distance upstream to look for overlap',
    type=int,
    default=0)
parser.add_argument(
    '--downstream',
    help='Distance downstream from gene to look for overlap',
    type=int,
    default=0)
parser.add_argument(
    '--body',
    help='Also look for overlap over the body of the feature',
    action='store_true',
    default=False)

gff_file = parser.parse_args().gff
ssreport = parser.parse_args().ssreport
gff_feature = parser.parse_args().feature
upstream = parser.parse_args().upstream
body = parser.parse_args().body
downstream = parser.parse_args().downstream
overlap_file = ssreport.rsplit('.', 1)[0] + (
    '_overlap_' + gff_feature + '_' + str(upstream) + '_up_' +
    str(downstream) + '_down_' + str(body).lower() + '_body.txt')

# Run the functions to get the overlap

gff_dict = parse_gff(gff_file, gff_feature)
shortstack_dict = parse_shortstack_full_report(ssreport)

overlap_shortstack_gff3(
    gff_dict, shortstack_dict, upstream, body, downstream, overlap_file)

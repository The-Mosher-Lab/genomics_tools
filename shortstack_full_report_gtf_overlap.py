#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Find small RNA clusters from a ShortStack "full report" file that
# overlap with features in a gtf file.
# Created: 10/2017

import csv
from argparse import ArgumentParser

# Parsing and overlap functions here


def parse_gtf(input_gtf, gtf_feature):
    gtf_dict = {}
    with open(input_gtf, 'r') as input_handle:
        input_reader = csv.reader(input_handle, delimiter='\t')
        for row in input_reader:
            if row[2] == gtf_feature:
                chromosome = row[0]
                start = int(row[3])
                stop = int(row[4])
                feature_id = str(row[8].split(';')[0])[8:]
                if chromosome not in gtf_dict:
                    gtf_dict[chromosome] = {}
                if feature_id not in gtf_dict[chromosome]:
                    gtf_dict[chromosome][feature_id] = {}
                gtf_dict[chromosome][feature_id] = [start, stop]
        return gtf_dict


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
            if chromosome not in shortstack_dict:
                shortstack_dict[chromosome] = {}
            if cluster_name not in shortstack_dict[chromosome]:
                shortstack_dict[chromosome][cluster_name] = [
                    cluster_start, cluster_stop]
    return shortstack_dict


def overlap_shortstack_gtf(gtf_dict, shortstack_dict, upstream_bp,
                           feature_body, downstream_bp, output_file):
    overlap_header = ['upstream', 'body', 'downstream']
    upstream_overlaps = 0
    downstream_overlaps = 0
    body_overlaps = 0
    with open(output_file, 'w') as output_handle:
        output_writer = csv.writer(output_handle)
        output_writer.writerow(overlap_header)
        for chromosome in gtf_dict:
            if chromosome in shortstack_dict:
                for feature in gtf_dict[chromosome]:
                    feature_start = gtf_dict[chromosome][feature][0]
                    feature_stop = gtf_dict[chromosome][feature][1]
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
    '--gtf', help='Input gtf file', metavar='File')
parser.add_argument(
    '--ssreport', help='Input ShortStack Report', metavar='File')
parser.add_argument(
    '--feature',
    help='Feature to look for overlap with from gtf file',
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

gtf_file = parser.parse_args().gtf
ssreport = parser.parse_args().ssreport
gtf_feature = parser.parse_args().feature
upstream = parser.parse_args().upstream
body = parser.parse_args().body
downstream = parser.parse_args().downstream
overlap_file = ssreport.rsplit('.', 1)[0] + (
    '_overlap_' + gtf_feature + '_' + str(upstream) + '_up_' +
    str(downstream) + '_down_' + str(body).lower() + '_body.csv')

# Run the functions to get the overlap

gtf_dict = parse_gtf(gtf_file, gtf_feature)
shortstack_dict = parse_shortstack_full_report(ssreport)

overlap_shortstack_gtf(
    gtf_dict, shortstack_dict, upstream, body, downstream, overlap_file)

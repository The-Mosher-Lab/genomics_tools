#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Find overlap with shortstack loci and features in a gtf, gff3, or
# deseq2 results.
# Created: 10/2017

import csv
from argparse import ArgumentParser

# Parsing and overlap functions here


def parse_shortstack_full_report(input_report):
    shortstack_dict = {}
    with open(input_report, 'r') as input_handle:
        input_reader = csv.reader(input_handle)
        next(input_reader)
        for row in input_reader:
            chromosome = row[0].split(':')[0]
            start = int(row[0].split(':')[1].split('-')[0])
            stop = int(row[0].split(':')[1].split('-')[1])
            name = row[1]
            if chromosome not in shortstack_dict:
                shortstack_dict[chromosome] = {}
            shortstack_dict[chromosome][name] = [start, stop]
    return shortstack_dict


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
                gtf_dict[chromosome][feature_id] = [start, stop]
        return gtf_dict


def parse_gff(input_gff, gff_feature):
    gff_dict = {}
    with open(input_gff, 'r') as input_handle:
        input_file = csv.reader(
            (row for row in input_handle if not row.startswith('#')),
            delimiter='\t')
        for row in input_file:
            if row[2] == gff_feature:
                chromosome = row[0]
                start = int(row[3])
                stop = int(row[4])
                feature_id = str(row[8].split(';')[0])[3:]
                if chromosome not in gff_dict:
                    gff_dict[chromosome] = {}
                gff_dict[chromosome][feature_id] = [start, stop]
        return gff_dict


def parse_deseq2_results(deseq2_results):
    results_dict = {}
    with open(deseq2_results, 'r') as input_handle:
        input_reader = csv.reader(input_handle)
        next(input_reader)
        for row in input_reader:
            chromosome = row[0]
            feature_id = row[1]
            start = int(row[3])
            stop = int(row[4])
            if chromosome not in results_dict:
                results_dict[chromosome] = {}
            results_dict[chromosome][feature_id] = [start, stop]
    return results_dict


def overlap_shortstack_features(anno_dict, shortstack_dict, upstream_bp,
                                feature_body, downstream_bp, output_file):
    overlap_header = ['upstream', 'body', 'downstream']
    upstream_overlaps = 0
    downstream_overlaps = 0
    body_overlaps = 0
    with open(output_file, 'w') as output_handle:
        output_writer = csv.writer(output_handle)
        for chromosome in anno_dict:
            if chromosome in shortstack_dict:
                for feature_id in anno_dict[chromosome]:
                    feature_start = anno_dict[chromosome][feature_id][0]
                    feature_stop = anno_dict[chromosome][feature_id][1]
                    for cluster in shortstack_dict[chromosome]:
                        cluster_start = shortstack_dict[chromosome][cluster][0]
                        if (upstream_bp > 0 and feature_start - upstream_bp <=
                                cluster_start <= feature_start):
                            upstream_overlaps += 1
                        if (feature_body and feature_start <= cluster_start <=
                                feature_stop):
                            body_overlaps += 1
                        if (downstream_bp > 0 and feature_stop + downstream_bp
                                >= cluster_start >= feature_stop):
                            downstream_overlaps += 1
        overlaps = [upstream_overlaps, body_overlaps, downstream_overlaps]
        print(overlap_header)
        print(overlaps)
        output_writer.writerow(overlap_header)
        output_writer.writerow(overlaps)


# Parse command line options

parser = ArgumentParser(
    description='Look for overlap with shortstack loci and gtf/gff3 '
    'features or deseq2 differentially expressed features annotated with start'
    ' and stop coordinates by deseq2_results_gff_annotate.py')
parser.add_argument(
    '-a',
    '--anno_type',
    help='Type of annotation, either gff3, gtf, or deseq2',
    choices=('gff3', 'gtf', 'deseq2'))
parser.add_argument(
    '-g',
    '--anno_file',
    help='Input gff3, gtf, or deseq2 results file',
    metavar='File')
parser.add_argument(
    '-f',
    '--feature',
    help='Feature to look for overlap with from gtf3 file',
    type=str)
parser.add_argument(
    '-l',
    '--ssloci',
    help='Input ShortStack loci file (.tsv/.csv)',
    metavar='File')
parser.add_argument(
    '-u',
    '--upstream',
    help='Distance upstream to look for overlap',
    metavar='bp',
    type=int,
    default=0)
parser.add_argument(
    '-d',
    '--downstream',
    help='Distance downstream from gene to look for overlap',
    metavar='bp',
    type=int,
    default=0)
parser.add_argument(
    '-b',
    '--body',
    help='Also look for overlap over the body of the feature',
    action='store_true',
    default=False)

anno_type = parser.parse_args().anno_type
anno_file = parser.parse_args().anno_file
feature = parser.parse_args().feature
loci_file = parser.parse_args().ssloci
upstream = parser.parse_args().upstream
body = parser.parse_args().body
downstream = parser.parse_args().downstream
output_file = loci_file.split('.')[0] + (
    '_' + anno_type + '_' + feature + '_overlap_' + str(upstream) + '_up_' +
    str(downstream) + '_down_' + str(body).lower() + '_body.csv')

# Run the functions to get the overlaps

shortstack_dict = parse_shortstack_full_report(loci_file)
if anno_type == 'gtf':
    anno_dict = parse_gtf(anno_file, feature)
elif anno_type == 'gff3':
    anno_dict = parse_gff(anno_file, feature)
elif anno_type == 'deseq2':
    anno_dict = parse_deseq2_results(anno_file)

overlap_shortstack_features(anno_dict, shortstack_dict, upstream, body,
                            downstream, output_file)

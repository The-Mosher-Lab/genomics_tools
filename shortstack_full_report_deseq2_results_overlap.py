#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Find small RNA clusters from a ShortStack "full report" file that
# overlap with differentially expressed genes from DESeq2 results that have
# coordinate information added by deseq2_results_results_annotate.py
# Created: 10/2017

import csv
from argparse import ArgumentParser

# Parsing and overlap functions here


def get_header(input_file):
    with open(input_file, 'r') as input_handle:
        input_reader = csv.reader(input_handle)
        header = next(input_reader)
        return header


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


def parse_deseq2_results(input_deseq2_results):
    results_dict = {}
    with open(input_deseq2_results, 'r') as input_handle:
        input_reader = csv.reader(input_handle)
        next(input_reader)
        for row in input_reader:
            chromosome = row[0]
            feature_id = row[1]
            feature_type = row[2]
            feature_start = int(row[3])
            feature_stop = int(row[4])
            deseq2_info = row[6:]
            if chromosome not in results_dict:
                results_dict[chromosome] = {}
            if feature_id not in results_dict[chromosome]:
                results_dict[chromosome][feature_id] = [
                    feature_start, feature_stop, feature_type
                ] + deseq2_info
    return results_dict


def overlap_shortstack_results(results_dict, shortstack_dict, upstream_bp,
                               downstream_bp, feature_body, output_file,
                               results_header, shortstack_header):
    with open(output_file, 'w') as output_handle:
        output_writer = csv.writer(output_handle)
        feature_separator = '#'
        results_header[0] = '#' + results_header[0]
        output_writer.writerow(results_header)
        output_writer.writerow(shortstack_header)
        for chromosome in results_dict:
            if chromosome in shortstack_dict:
                for feature_id in results_dict[chromosome]:
                    feature_start = results_dict[chromosome][feature_id][0]
                    feature_stop = results_dict[chromosome][feature_id][1]
                    feature_type = results_dict[chromosome][feature_id][2]
                    deseq2_info = results_dict[chromosome][feature_id][3:]
                    feature_row = [
                        feature_separator + chromosome, feature_id,
                        feature_start, feature_stop, feature_type
                    ] + deseq2_info
                    output_writer.writerow(feature_row)
                    for cluster in shortstack_dict[chromosome]:
                        cluster_start = shortstack_dict[chromosome][cluster][0]
                        cluster_stop = shortstack_dict[chromosome][cluster][1]
                        shortstack_info = shortstack_dict[chromosome][cluster][
                            2:]
                        cluster_row = [
                            chromosome, cluster, cluster_start, cluster_stop
                        ] + shortstack_info
                        if upstream_bp > 0 and feature_start - upstream_bp <= cluster_start <= feature_start:
                            output_writer.writerow(cluster_row)
                        if feature_body and feature_start <= cluster_start <= feature_stop:
                            output_writer.writerow(cluster_row)
                        if downstream_bp > 0 and feature_stop + downstream_bp >= cluster_start >= feature_stop:
                            output_writer.writerow(cluster_row)


# Parse command line options

parser = ArgumentParser(
    description='Looks for overlap between features in a DESeq2 results file '
    'and siRNA clusters defined by ShortStack')
parser.add_argument(
    '--results', help='Input ShortStack Results file', metavar='File')
parser.add_argument(
    '--ssreport', help='Input ShortStack Report', metavar='File')
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

results_file = parser.parse_args().results
ssreport = parser.parse_args().ssreport
upstream = parser.parse_args().upstream
body = parser.parse_args().body
downstream = parser.parse_args().downstream
overlap_file = ssreport.rsplit(
    '.', 1)[0] + ('_overlap_results_' + str(upstream) + '_up_' +
                  str(downstream) + '_down_' + str(body).lower() + '_body.txt')

# Run the functions to get the overlap

shortstack_dict = parse_shortstack_full_report(ssreport)
shortstack_header = ['chromosome', 'cluster_name', 'start', 'stop'
                     ] + get_header(ssreport)[2:]
results_dict = parse_deseq2_results(results_file)
results_header = get_header(results_file)

overlap_shortstack_results(results_dict, shortstack_dict, upstream, downstream,
                           body, overlap_file, results_header,
                           shortstack_header)

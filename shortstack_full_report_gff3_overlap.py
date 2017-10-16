#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Find small RNA clusters from a ShortStack "full report" file that overlap with features in a gff3
# Created: 10/2017

import csv
from argparse import ArgumentParser


# Define function to create a dictionary of gff3 features of interest

def parse_gff(input_gff, gff_feature):
    gff_dict = {}
    with open(input_gff, 'r') as input_handle:
        input_file = csv.reader((row for row in input_handle if not row.startswith('#')), delimiter='\t')
        for row in input_file:
            if row[2] == gff_feature:
                chromosome = row[0]
                feature = row[2]
                start = int(row[3])
                stop = int(row[4])
                strand = row[5]
                feature_id = str(row[8].split(';')[0])[3:]  # Store ID without ID=Bra as an integer
                if chromosome not in gff_dict:
                    gff_dict[chromosome] = {}
                gff_dict[chromosome] = [feature_id, feature, start, stop, strand]
        return gff_dict


def parse_shortstack_full_report(input_report):
    shortstack_dict = {}
    with open(input_report, 'r') as input_handle:
        input_file = csv.reader(row for row in input_handle if not row.startswith('#'))
        for row in input_file:
            chromosome = row[0].split(':')[0]
            start = int(row[0].split(':')[1].split('-')[0])
            stop = int(row[0].split(':')[1].split('-')[1])
            cluster_name = row[1]
            to_row_end = row[2:]
            if chromosome not in shortstack_dict:
                shortstack_dict[chromosome] = {}
            shortstack_dict[chromosome] = [cluster_name, start, stop, to_row_end]
        return shortstack_dict


def overlap_shortstack_gff3(gff_dict, shortstack_dict, output_file, upstream_bp):
    with open(output_file, 'a') as output_handle:
        for chromosome in gff_dict:
            if chromosome in shortstack_dict:
                for gene in gff_dict[chromosome]:
                    gene_id = gene[0]
                    feature = gene[1]
                    gene_start = gene[2]
                    gene_stop = gene[3]
                    gene_strand = gene[4]
                    output_handle.write(','.join('###', chromosome, gene_id, feature, gene_start, gene_stop, gene_strand))
                    for cluster in shortstack_dict[chromosome]:
                        cluster_name = cluster[0]
                        cluster_start = cluster[1]
                        cluster_stop = cluster[2]
                        cluster_info = cluster[3]
                        if cluster_start >= gene_start - upstream_bp:
                            output_handle.write(','.join(chromosome, cluster_start, cluster_stop, cluster_name, cluster_info))


# Parse command line options

parser = ArgumentParser(description='Looks for overlap between features of interest in a gff3 file and siRNA clusters from a ShortStack full_report')
parser.add_argument('--gff', help='Input gff3 file', metavar='File')
parser.add_argument('--ssreport', help='Input ShortStack Report', metavar='File')
parser.add_argument('--feature', help='Feature to look for overlap with from gff3 file', type=str)
parser.add_argument('--upstream', help='Distance upstream to look for overlap', type=int)
#parser.add_argument('--downstream', help='Distance downstream from gene to look for overlap', type=int)
#parser.add_argument('--body', help='Also look for overlap over the body of the feature')

gff = parser.parse_args().gff
ssreport = parser.parse_args().ssreport
gff_feature = parser.parse_args().feature
upstream = parser.parse_args().upstream
overlap_file = 'overlap.txt'

# Run the functions

overlap_shortstack_gff(parse_gff(gff, gff_feature), parse_shortstack_full_report(ssreport), overlap_file, upstream)

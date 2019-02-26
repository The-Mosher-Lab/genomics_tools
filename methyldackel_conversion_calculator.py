#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Determine bisulfite conversion rate from MethylDackel bedGraph files
# Created: 2/2019

import csv
from argparse import ArgumentParser

# Function block


def parse_bedgraph(input_context_bedgraph):
    met_count = 0
    unmet_count = 0
    with open(input_context_bedgraph, 'r') as input_handle:
        bedgraph_reader = csv.reader(input_handle, delimiter='\t')
        next(bedgraph_reader)  # Skip header
        for line in bedgraph_reader:
            met_count += int(line[4])
            unmet_count += int(line[5])
    return [met_count, unmet_count]


def conversion_calc(cg_counts, chg_counts, chh_counts):
    total_cg = cg_counts[0] + cg_counts[1]
    total_chg = chg_counts[0] + chg_counts[1]
    total_chh = chh_counts[0] + chh_counts[1]
    conversion_rate = ( sum((cg_counts[1], chg_counts[1], chh_counts[1])) /
                        sum((total_cg, total_chg, total_chh)) ) * 100
    print('CG Methylated/Total:\t', cg_counts[0], '/', total_cg)
    print('CHG Methylated/Total:\t', chg_counts[0], '/', total_chg)
    print('CHH Methylated/Total:\t', chh_counts[0], '/', total_chh)
    print('Conversion Rate:\t', conversion_rate)


# Command line parser

parser = ArgumentParser(
    description='Load CG, CHG, and CHH context bedGraph files from MethylDackel'
    'and calculate bisulfite conversion rate.')
parser.add_argument('--CG', help='CG Context bedGraph file.', metavar='File')
parser.add_argument('--CHG', help='CHG context bedGraph file.', metavar='File')
parser.add_argument('--CHH', help='CHH context bedGraph file.', metavar='File')

cg_bedgraph = parser.parse_args().CG
chg_bedgraph = parser.parse_args().CHG
chh_bedgraph = parser.parse_args().CHH

# Process the files

cg_counts = parse_bedgraph(cg_bedgraph)
chg_counts = parse_bedgraph(chg_bedgraph)
chh_counts = parse_bedgraph(chh_bedgraph)

conversion_calc(cg_counts, chg_counts, chh_counts)

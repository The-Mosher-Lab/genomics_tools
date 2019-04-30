#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Calculate percent methylation from MethylDackel bedGraph files
# Created: 2019-04-29

from argparse import ArgumentParser

# Function block


def methyl_calc(input_bedgraph):
    met_c = 0
    unmet_c = 0
    with open(input_bedgraph, 'r') as input_handle:
        next(input_handle)  # Skip header
        for line in input_handle:
            met_c += int(line.split()[4])
            unmet_c += int(line.split()[5])
    return (met_c / (met_c + unmet_c)) * 100


# Command line parser

parser = ArgumentParser(
    description='Calculate percent methylation from a set of MethylDackel '
    'bedGraphs files.')
parser.add_argument('--CG',
                    help='CG context bedGraph',
                    default=None,
                    metavar='File')
parser.add_argument('--CHG',
                    help='CHG context bedGraph',
                    default=None,
                    metavar='File')
parser.add_argument('--CHH',
                    help='CHH context bedGraph',
                    default=None,
                    metavar='File')

cg_bedgraph = parser.parse_args().CG
chg_bedgraph = parser.parse_args().CHG
chh_bedgraph = parser.parse_args().CHH

# Process the files

if not cg_bedgraph and not chg_bedgraph and not chh_bedgraph:
    print('Without data how do you expect to do anything!')
    exit
if cg_bedgraph:
    cg_methylation = methyl_calc(cg_bedgraph)
    print('CG Methylation', cg_methylation, sep='\t')
if chg_bedgraph:
    chg_methylation = methyl_calc(chg_bedgraph)
    print('CHG Methylation', chg_methylation, sep='\t')
if chh_bedgraph:
    chh_methylation = methyl_calc(chh_bedgraph)
    print('CHH Methylation', chh_methylation, sep='\t')

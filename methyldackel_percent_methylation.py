#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Calculate percent methylation from MethylDackel bedGraph files
# Created: 2019-04-29

from argparse import ArgumentParser
from sys import exit


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

def get_args():
    parser = ArgumentParser(
        description='Calculate percent methylation from a set of MethylDackel '
        'bedGraphs files.')
    parser.add_argument('--CG',
                        help='CG context bedGraph',
                        default=None,
                        metavar='FILE.bedGraph')
    parser.add_argument('--CHG',
                        help='CHG context bedGraph',
                        default=None,
                        metavar='FILE.bedGraph')
    parser.add_argument('--CHH',
                        help='CHH context bedGraph',
                        default=None,
                        metavar='FILE.bedGraph')
    return parser.parse_args()


# Process the files

def main(args):
    if not args.CG and not args.CHG and not args.CHH:
        exit('Without data how do you expect to do anything!')
    if args.CG:
        cg_methylation = methyl_calc(args.CG)
        print('CG', cg_methylation, sep='\t')
    if args.CHG:
        chg_methylation = methyl_calc(args.CHG)
        print('CHG', chg_methylation, sep='\t')
    if args.CHH:
        chh_methylation = methyl_calc(args.CHH)
        print('CHH', chh_methylation, sep='\t')


if __name__ == '__main__':
    main(get_args())

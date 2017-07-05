#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: To determine which small RNA loci are significantly reduced in each sample
# Created: 6/2017

# Outputs the number of loci dependent on each of the RdDM machinery to stdout. This code is embarrassingly ugly.

import csv
from argparse import ArgumentParser


# Define function to load a summary file with expression values for each sample and output the cluster name and
# location of loci significantly reduced in each sample

def dependence_test(input_file, significance):
    nrpd_dependent = 0
    nrpe_dependent = 0
    rdr2_dependent = 0
    nrpd_nrpe_dependent = 0
    nrpd_rdr2_dependent = 0
    nrpe_rdr2_dependent = 0
    nrpd_nrpe_rdr2_dependent = 0
    significance_threshold = 1 - (significance/100)
    with open(input_file, 'r') as input_handle:
        input_csv = csv.reader(input_handle, delimiter=',')
        next(input_csv)
        for row in input_csv:
            wt = float(row[3])
            nrpd = float(row[4])
            nrpe = float(row[5])
            rdr2 = float(row[6])
            if nrpd <= wt * significance_threshold:
                nrpd_dependent += 1
            if nrpe <= wt * significance_threshold:
                nrpe_dependent += 1
            if rdr2 <= wt * significance_threshold:
                rdr2_dependent += 1
            if nrpd <= wt * significance_threshold and nrpe <= wt * significance_threshold:
                nrpd_nrpe_dependent += 1
            if nrpd <= wt * significance_threshold and rdr2 <= wt * significance_threshold:
                nrpd_rdr2_dependent += 1
            if nrpe <= wt * significance_threshold and rdr2 <= wt * significance_threshold:
                nrpe_rdr2_dependent += 1
            if nrpd <= wt * significance_threshold and nrpe <= wt * significance_threshold and rdr2 <= wt * significance_threshold:
                nrpd_nrpe_rdr2_dependent += 1
    print('nrpd_dependent,%s' % nrpd_dependent)
    print('nrpe_dependent,%s' % nrpe_dependent)
    print('rdr2_dependent,%s' % rdr2_dependent)
    print('nrpd_nrpe_dependent,%s' % nrpd_nrpe_dependent)
    print('nrpd_rdr2_dependent,%s' % nrpd_rdr2_dependent)
    print('nrpe_rdr2_dependent,%s' % nrpe_rdr2_dependent)
    print('nrpd_nrpe_rdr2_dependent,%s' % nrpd_nrpe_rdr2_dependent)

# Parse command line options

parser = ArgumentParser(description='This outputs the number of loci dependent on each of the RdDM machinery. Very '
                                    'rough code.')
parser.add_argument('-s', '--significance', help='Percentage reduction to test', type=float)
parser.add_argument('input_path', help='Input file', metavar='File')

input_path = parser.parse_args().input_path
reduction_signifiance = parser.parse_args().significance

# Analyze the data

dependence_test(input_path, reduction_signifiance)

#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: To determine which small RNA loci are present above an expression threshold in a sample.
# Created: 6/2017

# Outputs the number of loci above an expression threshold to stdout. This code is embarrassingly ugly.

import csv
from argparse import ArgumentParser


# Define function to load a summary file with expression values for each sample and output the cluster name and
# location of loci present above a threshold in each sample

def dependence_test(input_file, significance):
    wt_present = 0
    nrpd_present = 0
    nrpe_present = 0
    rdr2_present = 0
    nrpd_nrpe_present = 0
    nrpd_rdr2_present = 0
    nrpe_rdr2_present = 0
    wt_nrpd_nrpe_present = 0
    wt_nrpd_rdr2_present = 0
    wt_nrpe_rdr2_present = 0
    nrpd_nrpe_rdr2_present = 0
    wt_nrpd_present = 0
    wt_nrpe_present = 0
    wt_rdr2_present = 0
    wt_nrpd_nrpe_rdr2_present = 0
    significance_threshold = 1 - (significance/100)
    with open(input_file, 'r') as input_handle:
        input_csv = csv.reader(input_handle, delimiter=',')
        next(input_csv)
        for row in input_csv:
            wt = float(row[3])
            nrpd = float(row[4])
            nrpe = float(row[5])
            rdr2 = float(row[6])
            if wt > 0:
                wt_present += 1
            if nrpd >= wt * significance_threshold:
                nrpd_present += 1
            if nrpe >= wt * significance_threshold:
                nrpe_present += 1
            if rdr2 >= wt * significance_threshold:
                rdr2_present += 1
            if nrpd >= wt * significance_threshold and nrpe >= wt * significance_threshold:
                nrpd_nrpe_present += 1
            if nrpd >= wt * significance_threshold and rdr2 >= wt * significance_threshold:
                nrpd_rdr2_present += 1
            if nrpe >= wt * significance_threshold and rdr2 >= wt * significance_threshold:
                nrpe_rdr2_present += 1
            if nrpd >= wt * significance_threshold and nrpe >= wt * significance_threshold and rdr2 >= wt * significance_threshold:
                nrpd_nrpe_rdr2_present += 1
            if wt > 0 and nrpd >= wt * significance_threshold:
                wt_nrpd_present += 1
            if wt > 0 and nrpe >= wt * significance_threshold:
                wt_nrpe_present += 1
            if wt > 0 and rdr2 >= wt * significance_threshold:
                wt_rdr2_present += 1
            if wt > 0 and nrpd >= wt * significance_threshold and nrpe >= wt * significance_threshold:
                wt_nrpd_nrpe_present += 1
            if wt > 0 and nrpd >= wt * significance_threshold and rdr2 >= wt * significance_threshold:
                wt_nrpd_rdr2_present += 1
            if wt > 0 and nrpe >= wt * significance_threshold and rdr2 >= wt * significance_threshold:
                wt_nrpe_rdr2_present += 1
            if wt > 0 and nrpd >= wt * significance_threshold and nrpe >= wt * significance_threshold and rdr2 >= wt * significance_threshold:
                wt_nrpd_nrpe_rdr2_present += 1
    print('wt_present,%s' % wt_present)
    print('wt_nrpd_present,%s' % wt_nrpd_present)
    print('wt_nrpe_present,%s' % wt_nrpe_present)
    print('wt_rdr2_present,%s' % wt_rdr2_present)
    print('wt_nrpd_nrpe_present,%s' % wt_nrpd_nrpe_present)
    print('wt_nrpd_nrpe_rdr2_present,%s' % wt_nrpd_nrpe_rdr2_present)
    print('nrpd_present,%s' % nrpd_present)
    print('nrpe_present,%s' % nrpe_present)
    print('rdr2_present,%s' % rdr2_present)
    print('nrpd_nrpe_present,%s' % nrpd_nrpe_present)
    print('nrpd_rdr2_present,%s' % nrpd_rdr2_present)
    print('nrpe_rdr2_present,%s' % nrpe_rdr2_present)
    print('nrpd_nrpe_rdr2_present,%s' % nrpd_nrpe_rdr2_present)
    print('wt_nrpd_rdr2_present,%s' % wt_nrpd_rdr2_present)
    print('wt_nrpe_rdr2_present,%s' % wt_nrpe_rdr2_present)


# Parse command line options

parser = ArgumentParser(description='This outputs the number of loci present in each genotype above some expression '
                                    'threshold in wild-type (sample #1). Very rough code.')
parser.add_argument('-s', '--significance', help='Percentage reduction to test', type=float)
parser.add_argument('input_path', help='Input file', metavar='File')

input_path = parser.parse_args().input_path
reduction_signifiance = parser.parse_args().significance

# Analyze the data

dependence_test(input_path, reduction_signifiance)

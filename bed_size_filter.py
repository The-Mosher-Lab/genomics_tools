#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Filter a bed file for entries of the size you wish
# Created: 2019-03-25

from argparse import ArgumentParser


# Simple .bed format parsing function here

def parse_bed(input_bed, min_size, max_size):
    with open(input_bed, 'r') as input_handle:
        for line in input_handle:
            start = int(line.split()[1])
            stop = int(line.split()[2])
            length = stop - start
            if length >= min_size and length <= max_size:
                print(line, end='')


# Parse command line options

parser = ArgumentParser(
    description='Filter a .bed file for entries within a range of sizes')
parser.add_argument('input_path',
                    help='File to process',
                    metavar='File')
parser.add_argument('--max_size',
                    '-m',
                    help='Max size (default 1e9, basically infinite)',
                    type=int,
                    default=1e9,
                    metavar='Integer')
parser.add_argument('--min_size',
                    '-n',
                    help='Min size (default 0)',
                    type=int,
                    default=0,
                    metavar='Integer')

input_path = parser.parse_args().input_path
max_size = parser.parse_args().max_size
min_size = parser.parse_args().min_size

# Process the file

parse_bed(input_path, min_size, max_size)

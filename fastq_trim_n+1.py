#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Remove the artifact n+1 bases from the ends of reads in a fastq
# Created: 01/2019

from argparse import ArgumentParser


def trim_ends(input_path, target_length):
    n = 0
    data_lines = (line.rstrip() for line in open(input_path, 'r'))
    for line in data_lines:
        n += 1
        if n == 2:
            if len(line) == (target_length + 1):
                print(line[:-1])
            else:
                print(line)
        elif n == 4:
            if len(line) == (target_length + 1):
                print(line[:-1])
            else:
                print(line)
            n = 0
        else:
            print(line)


# Parse command line options

parser = ArgumentParser(
    description='Trims 1 base (and q score) from the end of reads in a fastq '
    'file when the length is readlength + 1. This was created to deal with the '
    'n + 1 readlength errors, without trimming good bases from shorter reads.')
parser.add_argument('input_path', help='Input .fastq file', metavar='File')
parser.add_argument(
    '-t', '--target_length', help='Target length for the reads', type=int)

input_fastq = parser.parse_args().input_path
target_length = parser.parse_args().target_length

# Trim the fastq

trim_ends(input_fastq, target_length)

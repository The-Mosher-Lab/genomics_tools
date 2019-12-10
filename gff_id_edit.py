#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Edit fields within a gff file
# Created: 2019-12-09
# Disclaimer: Works when I needed it to, I make no promises about other purposes

from argparse import ArgumentParser


# Define function to parse and convert a gff3

def gff_edit(input_gff, chr_append, id_append):
    with open(input_gff, 'r') as input_handle:
        for line in input_handle:
            if not line == '\n' and not line.startswith('#'):
                entry = line.strip().split()
                entry[0] = entry[0] + chr_append
                attr = entry[8].split(';')
                for i, k in enumerate(attr):
                    attr[i] = k + id_append
                print(*entry[0:7], sep='\t', end='\t')
                print(*attr, sep=';')


# Parse command line options

def get_args():
    parser = ArgumentParser(
        description='Convert chromosome and gene IDs in a gff3 file to add stuff to them')
    parser.add_argument(
        'gff',
        help='A gff3 file to convert',
        metavar='FILE.gff3')
    parser.add_argument(
        '-c', '--chr_append',
        help='String to append to chromosome IDs',
        metavar='STRING')
    parser.add_argument(
        '-i', '--id_append',
        help='String to append to gene IDs',
        metavar='STRING')
    return parser.parse_args()


# Convert the file

def main(args):
    gff_edit(args.gff, args.chr_append, args.id_append)


if __name__ == '__main__':
    main(get_args())

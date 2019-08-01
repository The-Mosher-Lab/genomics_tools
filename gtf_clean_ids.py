#!/usr/bin/env python3
# Author: Jeffrey Grover
# Purpose: Clean garbage from gtf files in the chromosome ID and gene ID fields
# Created: 09/2018

# Note, this was created in a hurry, and worked for the one use case I made it
# for. However, use at your own risk. GTF/GFF format is notoriously nonstandard

from argparse import ArgumentParser


def clean_gtf(input_file, cleaner_sep, chromosome, feature):
    with open(input_file, 'r') as input_handle:
        for line in input_handle:
            entry = line.strip().split('\t')
            if chromosome:
                entry[0] = entry[0].split(cleaner_sep)[0]
            group = entry[8].split('; ')
            if feature:
                transcript_id = group[0].split(cleaner_sep)[0]
                gene_id = group[1].split(cleaner_sep)[0]
                gene_name = group[2].split(cleaner_sep)[0]
                group = [transcript_id, gene_id, gene_name]
            print('\t'.join(entry[0:8]), end='\t')
            print('"; '.join(group), end='"\n')


# Parse command line options


def get_args():
    parser = ArgumentParser(
        description='Removes garbage from chromosome and gene IDs in a gtf.')
    parser.add_argument('gtf', help='File to process', metavar='FILE.gtf')
    parser.add_argument('--sep', '-s', help='Separator to remove text after')
    parser.add_argument('--chromosome', '-c',
                        help='Clean chromosome IDs',
                        action='store_true')
    parser.add_argument('--feature', '-f',
                        help='Clean feature IDs',
                        action='store_true')
    return parser.parse_args()


# Process file


def main(args):
    clean_gtf(args.gtf, args.sep, args.chromosome, args.feature)


if __name__ == '__main__':
    main(get_args())

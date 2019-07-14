#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Filter the output from NCBI Blast+ format #7 or 6
# Created: 2019-07-13


from argparse import ArgumentParser


# Filter and output line by line

def filter_blast7(input_blast_results, min_perc_id, min_al_len, max_evalue):
    with open(input_blast_results, 'r') as input_handle:
        header = ('# query', 'subject', 'perc_identity', 'alignment_length',
                  'mismatches', 'gap_opens', 'q_start', 'q_end', 's_start',
                  's_end', 'evalue', 'bit_score')
        print('\t'.join(header))
        for line in input_handle:
            if not line.startswith('#'):
                entry = line.strip().split()
                perc_id = float(entry[2])
                al_len = int(entry[3])
                evalue = float(entry[10])
                if (
                    perc_id >= min_perc_id
                    and al_len >= min_al_len
                    and evalue <= max_evalue
                ):
                    print('\t'.join(entry))


def get_args():
    parser = ArgumentParser(
        description='Filter the output from NCBI BLAST+ based on criteria.'
        ' Currently works with format type 6 and 7 only.')
    parser.add_argument(
        'blast_output',
        help='Output from NCBI BLAST+ in format type 7',
        metavar='FILE')
    parser.add_argument(
        '-i', '--min_id',
        help='Minimum percent identity',
        type=float,
        metavar='ID')
    parser.add_argument(
        '-l', '--min_len',
        help='Minimum alignment length',
        type=int,
        metavar='LENGTH')
    parser.add_argument(
        '-e', '--max_evalue',
        help='Maximum e-evalue',
        type=float,
        metavar='EVALUE')
    return parser.parse_args()


def main(args):
    filter_blast7(args.blast_output, args.min_id, args.min_len, args.max_evalue)


if __name__ == '__main__':
    main(get_args())

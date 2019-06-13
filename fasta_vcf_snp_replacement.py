#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Create a genome where SNPs from a .vcf have been placed into the
# .fasta at the appropriate places
# Created: 2019/03/13

from argparse import ArgumentParser
from itertools import groupby
from sys import exit

# Functions


def fasta_iterate(fasta_file):
    with open(fasta_file, 'r') as reader:
        fasta_reader = (
            x[1] for x in groupby(reader, lambda line: line.startswith('>')))
        for header in fasta_reader:
            chromosome = next(header).strip('>').rstrip('\n')
            seq = ''.join(s.strip() for s in next(fasta_reader))
            yield (chromosome, seq)


def parse_snps_to_dict(vcf_file):
    snps_dict = {}
    with open(vcf_file, 'r') as vcf_reader:
        for line in vcf_reader:
            if not line.startswith('#'):
                vcf_record = line.split('\t')
                chromosome = vcf_record[0]
                position = int(vcf_record[1])
                ref_base = vcf_record[3]
                alt_base = vcf_record[4]
                if chromosome not in snps_dict:
                    snps_dict[chromosome] = {}
                if position in snps_dict[chromosome]:
                    exit('Error: .vcf files should have exactly one call per position.')
                else:
                    snps_dict[chromosome][position] = (ref_base, alt_base)
    return snps_dict


def wrap_text(text, width=80):
    for s in range(0, len(text), width):
        yield text[s:s+width]


def replace_snps(fasta_iterator, snps_dict, output_fasta, genotype):
    with open(output_fasta, 'w') as fasta_writer:
        for chromosome, seq in fasta_iterator:
            fasta_header = '>%s_%s' % (chromosome, genotype)
            bases = list(seq)
            fasta_writer.write(fasta_header + '\n')
            if chromosome in snps_dict:
                for position in snps_dict[chromosome]:
                    if snps_dict[chromosome][position][0] == bases[(position - 1)]:  # Due to 1-based coordinate system
                        bases[(position - 1)] = snps_dict[chromosome][position][1]
                    else:
                        exit('Error: .vcf reference base and fasta mismatch.')
            for line in wrap_text(''.join(bases)):
                fasta_writer.write(line)


# CLI argument parser


def get_args():
    parser = ArgumentParser(
        description='Replace SNPs from a .vcf file into the correct positions '
        'in a .fasta file.')
    parser.add_argument(
        '-f',
        '--fasta',
        help='An input fasta file to use as a reference',
        metavar='FILE')
    parser.add_argument(
        '-v',
        '--vcf',
        help='An input .vcf file with exactly one variant per position.',
        metavar='FILE')
    parser.add_argument(
        '-g',
        '--genotype',
        help='A string which will be added to the chromosome IDs and output '
        'file-name indicating the genotype of the SNPs.',
        metavar='STRING')

    return parser.parse_args()


# Main function entry point


def main(args):

    # Set the output filename

    output_fasta = args.fasta.rsplit('.', 1)[0] + '.%s.snps.fa' % args.genotype

    # Process the .fasta and .vcf

    snps_dict = parse_snps_to_dict(args.vcf)
    replace_snps(fasta_iterate(args.fasta), snps_dict, output_fasta, args.genotype)


if __name__ == "__main__":
    args = get_args()
    main(args)

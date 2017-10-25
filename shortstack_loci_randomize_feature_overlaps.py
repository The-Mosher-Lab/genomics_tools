#!/usr/bin/env python3

# Author: Jeffrey Grover
# Purpose: Randomize siRNA loci defined by ShortStack to look for overlaps with
# features. Provides a measure of significance for differentially expressed
# features which overlap siRNA clusters
# Created: 10/2017

import csv
import random
from argparse import ArgumentParser
from itertools import groupby

# Functions


def get_shortstack_clusters(loci_tsv):
    shortstack_loci = []
    with open(loci_tsv, 'r') as input_handle:
        reader = csv.reader(input_handle, delimiter='\t')
        next(reader)  # Skip header
        for row in reader:
            cluster_name = row[1]
            cluster_start = int(row[0].split(':')[1].split('-')[0])
            cluster_stop = int(row[0].split(':')[1].split('-')[1])
            cluster_length = cluster_stop - cluster_start
            cluster_record = [cluster_name, cluster_length]
            shortstack_loci.append(cluster_record)
    return shortstack_loci


def get_chromosome_lengths(fasta_file):
    chr_lengths = []
    with open(fasta_file, 'r') as input_handle:
        for is_header, group in groupby(input_handle,
                                        lambda x: x.startswith('>')):
            if is_header:
                # Sequence header is the first line, only want chromosome name
                chromosome = next(group).strip('>').rstrip('\n')
            else:
                # Join the sequence lines due to wrapping and get their length
                seq_length = len(''.join(group).replace('\n', ''))
                record = [chromosome, seq_length]
                chr_lengths.append(record)
    return chr_lengths


def get_randomized_clusters(shortstack_loci, chr_lengths):
    randomized_clusters = {}
    for cluster in shortstack_loci:
        cluster_name = cluster[0]
        cluster_length = cluster[1]
        while True:  # Gross hacky way of doing this
            random_record = random.choice(chr_lengths)
            chromosome = random_record[0]
            seq_length = random_record[1]
            if seq_length > cluster_length:
                break
        randomized_cluster_start = random.randint(0,
                                                  seq_length - cluster_length)
        randomized_cluster_stop = randomized_cluster_start + cluster_length
        if chromosome not in randomized_clusters:
            randomized_clusters[chromosome] = {}
        if cluster_name not in randomized_clusters[chromosome]:
            randomized_clusters[chromosome][cluster_name] = [
                randomized_cluster_start, randomized_cluster_stop,
                cluster_length
            ]
    return randomized_clusters


def parse_deseq2_results(input_deseq2_results):
    results_dict = {}
    with open(input_deseq2_results, 'r') as input_handle:
        input_reader = csv.reader(input_handle)
        next(input_reader)
        for row in input_reader:
            chromosome = row[0]
            feature_id = row[1]
            feature_start = int(row[3])
            feature_stop = int(row[4])
            if chromosome not in results_dict:
                results_dict[chromosome] = {}
            if feature_id not in results_dict[chromosome]:
                results_dict[chromosome][feature_id] = [
                    feature_start, feature_stop
                ]
    return results_dict


def overlap_randomized_clusters_results(results_dict, randomized_clusters,
                                        upstream_bp, downstream_bp,
                                        feature_body):
    upstream_overlaps = 0
    downstream_overlaps = 0
    body_overlaps = 0
    for chromosome in results_dict:
        if chromosome in randomized_clusters:
            for feature_id in results_dict[chromosome]:
                feature_start = results_dict[chromosome][feature_id][0]
                feature_stop = results_dict[chromosome][feature_id][1]
                for cluster in randomized_clusters[chromosome]:
                    cluster_start = randomized_clusters[chromosome][cluster][0]
                    cluster_stop = randomized_clusters[chromosome][cluster][1]
                    if upstream_bp > 0 and feature_start - upstream_bp <= cluster_start <= feature_start:
                        upstream_overlaps += 1
                    if feature_body and feature_start <= cluster_start <= feature_stop:
                        body_overlaps += 1
                    if downstream_bp > 0 and feature_stop + downstream_bp >= cluster_start >= feature_stop:
                        downstream_overlaps += 1
    print([upstream_overlaps, body_overlaps, downstream_overlaps])
    return [upstream_overlaps, body_overlaps, downstream_overlaps]


loci_tsv = 'WT_ovule_2rpm_mincov_75_pad_loci.tsv'
fasta_file = 'ro18_v1.2.fa'

shortstack_loci = get_shortstack_clusters(loci_tsv)
chr_lengths = get_chromosome_lengths(fasta_file)
randomized_clusters = get_randomized_clusters(shortstack_loci, chr_lengths)
results = parse_deseq2_results('results_fert_4-fold_padj_1e-12_annotated.csv')
overlap_randomized_clusters_results(results, randomized_clusters, 1000, 1000, True)

#! /usr/bin/env bash

# Author: Jeffrey Grover
# Created: 9/2017
# Purpose: Batch process the alignments I have to count reads over TEs using manually generated GTF files

# This script will run htseq-count on all .bam alignments in the same directory and count read overlaps with the indicated .gtf file.
# It sends the output to separate .counts files for each input.
# This uses GNU Parallel to run 10 processes at the same time. Each run requires a process for samtools and htseq-count, so in total 20 processes.

mkdir -p ./te_overlaps_htseq

ls *.bam | parallel --eta -j 10 --noswap 'samtools view -h {} | python3 -m HTSeq.scripts.count -m union -s no -t transposable_element -i gene_id - /home/groverj3/large_data/freeling_lab_TE_ro18_annotations/L9/ro18_te_repeatmasker_no_thaliana_cds.gtf > "./te_overlaps_htseq/{.}.counts"'

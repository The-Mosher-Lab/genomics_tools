#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 11/2017
# Purpose: Run bedtools window on a large number of files with randomized loci
# To get the counts of nearby and overlapped features

filename=$(basename "$1")
shuffled_dir="$2"
for bed_file in ${shuffled_dir}*.bed
do
    bedtools intersect -c -nonamecheck -a "$1" -b "$bed_file" | \
        awk '{sum+=$7;} END { print sum }' >> "${filename}_shuffled_overlaps.txt"
done

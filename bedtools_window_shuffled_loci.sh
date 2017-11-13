#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 11/2017
# Purpose: Run bedtools window on a large number of files with randomized loci
# To get the counts of nearby and overlapped features

# Pass through -l -r -a options in that order. Runs on all bed files in the same directory.

for bed_file in ./*.bed
do
    bedtools window -c -l "$1" -r "$2" -a "$3" -b "$bed_file" | \
    awk '{sum+=$7;} END { print sum }' >> "${3}_${1}_up_${2}_down_overlaps.txt"
done

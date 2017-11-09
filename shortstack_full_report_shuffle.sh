#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 11/2017
# Purpose: Use bedtools shuffle to randomly permute the positions of shortstack loci

# Takes three positional arguments because I'm too lazy to implement them as
# real commandline options. Runs bedtools shuffle the indicated number of times.

bootstraps=$1
input_file=$2
genome=$3
output_dir="./${input_file}_randomized_${bootstraps}_bootstraps/"
mkdir -p "$output_dir"
for ((i=1; i<=$bootstraps; i++))
do
    output_file="${output_dir}${input_file%.bam}_$i.bed"
    bedtools shuffle -noOverlapping -i "$input_file" -g "$genome" > \
    "$output_file"
done

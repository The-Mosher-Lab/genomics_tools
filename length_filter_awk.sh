#!/usr/bin/env bash

# Author: Jeffrey Grover
# Purpose: Filter .fastq reads between sizes defined by user input.

# The first option is minimum length, and second is maximum length.
# Run this script in a folder containing all the .fastq.gz files to be filtered.
# Outputs will go in a subdirectory called "filtered."

mkdir -p "./filtered_$1-$2" && \
for fastq_gz_file in ./*fastq.gz
do
	zcat "$fastq_gz_file" | awk -v min_length="$1" -v max_length="$2" '
    	BEGIN {
    	    OFS = "\n"
    	}
    	{
    	    header = $0 ; getline seq ; getline qheader ; getline qseq ; if (length(seq) >= min_length && length(seq) <= max_length) {
    	        print header, seq, qheader, qseq
    	        }
    	}
	' | gzip > "./filtered_$1-$2/${fastq_gz_file%.fastq.gz}.filtered.fastq.gz"
done
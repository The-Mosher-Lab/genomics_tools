#!/usr/bin/env bash

# Filter .fastq reads between sizes defined by user input.
# The first option passed is the file to run the script on, second is minimum length, and third is maximum length.

zcat "$1" | awk -v min_length="$2" -v max_length="$3" '
    BEGIN {
        OFS = "\n"
    }
    {
        header = $0 ; getline seq ; getline qheader ; getline qseq ; if (length(seq) >= min_length && length(seq) <= max_length) {
            print header, seq, qheader, qseq
            }
    }
' | gzip > "${1%.fastq.gz}.filtered.fastq.gz"
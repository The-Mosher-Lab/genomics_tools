#!/usr/bin/env bash

# Author: Jeffrey Grover
# Purpose: Reads fastq files and outputs counts of read lengths within the file

cat "$1" | awk '{if(NR%4==2) print length($1)}' | sort | uniq -c > "${1%.fastq}.readlengths.txt"
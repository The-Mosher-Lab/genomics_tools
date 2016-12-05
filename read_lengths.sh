#!/usr/bin/env bash

# Reads fastq files and outputs read lengths within the file

cat "$1" | awk '{if(NR%4==2) print length($1)}' | sort | uniq -c > "${1%.fastq}.readlengths.txt"
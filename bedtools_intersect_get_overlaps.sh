#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 11/2017
# Purpose: Run bedtools intersect to get the overlaps with features. 

# Uses the default behavior of only one required bp of overlap. Outputs counts.

file_a="$1"
file_b="$2"
output_file="$3"
bedtools intersect -nonamecheck -c -a "$file_a" -b "$file_b" > "$output_file"

#!/usr/bin/env bash

# Author: Jeffrey Grover
# Purpose: Filter .fastq reads between sizes defined by user input.
# Created: 12/2016

# Extracts reads from a .fastq file and creates a multifasta file from them using awk
# Reads from stdin and prints to stdout, you can pipe input from cat or zcat for example and redirect to an output file

awk 'BEGIN {OFS = "\n"} {header = $0 ; getline seq ; getline qheader ; getline qseq ; gsub(/^[@]/,">",header) ; print header, seq}' -
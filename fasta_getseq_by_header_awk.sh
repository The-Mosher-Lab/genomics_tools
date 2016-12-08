#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 12/2016
# Purpose: Pull fasta sequences based on a string from their header using awk

# Reads from stdin, so use cat/zcat, etc. Positional variable 1 = search string
# Outputs to stdout, so redirect to an output file of your choosing with "> filename.fa"

awk -v search_string="$1" 'BEGIN {RS=">"; ORS=""} $0 ~ search_string {print ">"$0}' -

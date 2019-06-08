#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 10/2017
# Purpose: Remove empty records from a fasta file

# Takes the input fastq as a command line argument

awk '$2{print RS $0}' FS='\n' RS="$1" ORS= ">"

#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 10/2017
# Purpose: Remove empty records from a fasta file or similar file with a record separator

# Takes two command line options, the record separator (in quotes) and the input file

awk '$2{print RS $0}' FS='\n' RS="$1" ORS= "$2"

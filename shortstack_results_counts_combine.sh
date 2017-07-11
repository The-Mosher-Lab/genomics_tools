#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 7/2017
# Purpose: Combine the shortstack output files; Results.txt and Counts.txt

# Accepts two filenames as input. File 1 will be Results.txt, File 2 is Counts.txt
# Outputs to a new file called "shortstack_full_report.txt"

join --header "$1" "$2" | cut -d ' ' --complement -f22,23 | tr ' ' ',' > shortstack_full_report.txt


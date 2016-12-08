#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 11/2016
# Purpose: Count number of chromosomes/contigs in a genome fasta

# Takes one command-line option as input file, outputs to stdout

fgrep -o ">" "$1" | wc -l
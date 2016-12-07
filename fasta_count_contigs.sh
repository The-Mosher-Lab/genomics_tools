#!/bin/bash

# Author: Jeffrey Grover
# Created: 11/2016
# Purpose: Count number of chromosomes/contigs in a genome fasta

fgrep -o ">" "$1" | wc -l
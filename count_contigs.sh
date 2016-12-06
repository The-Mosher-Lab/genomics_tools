#!/bin/bash

# Author: Jeffrey Grover, groverj3@gmail.com
# Purpose: Count number of chromosomes/contigs in a genome fasta

fgrep -o ">" "$1" | wc -l
#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 7/2017
# Purpose: Extract the first two columns from a shortstack "Results.txt" to a new file "loci.tsv" using GNU cut for simplicity

# Must be in the same folder as "Results.txt", outputs "loci.tsv"

cut -f 1-2 Results.txt > loci.tsv

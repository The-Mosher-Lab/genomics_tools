#!/bin/bash

# Count number of chromosomes/contigs in a genome fasta

fgrep -o ">" "$1" | wc -l
#!/usr/bin/env bash

# Author: Jeffrey Grover
# Purpose: Count reads in a .fastq file
# Created: 7/2017

# Counts reads in a .fastq file using wc -l by dividing the output by 4

echo $1 && \
expr $(cat $1 | wc -l) / 4

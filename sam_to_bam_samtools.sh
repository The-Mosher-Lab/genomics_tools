#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 02/2017
# Purpose: Reads sam files and converts to a sorted bam file

# Use 'find . -name "*.sam" -exec "./sam_to_bam_samtools.sh" {} \;' to batch process

samtools view -bS "$1" | samtools sort -o "${1%.sam}.bam" - 


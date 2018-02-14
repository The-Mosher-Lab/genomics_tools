#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 2/2018
# Purpose: Converts a .bam file to a .sam file using samtools

# Use 'find . -name "*.sam" -exec "./bam_to_sam_samtools" {} \;' to batch process

samtools view -h "$1" > "${1%.bam}.sam"


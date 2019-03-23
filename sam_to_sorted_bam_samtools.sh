#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 02/2017
# Purpose: Reads sam files and converts to a sorted bam file

# Can use find -exec or a loop to batch process

samtools view -bS "$1" | samtools sort -o "${1%.sam}.bam" - 


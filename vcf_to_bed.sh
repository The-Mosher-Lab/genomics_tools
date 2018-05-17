#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 5/2018
# Purpose: Convert .vcf files to .bed format

# Pass the .vcf to this script, outputs to stdout. Removes leading "chr."

sed -e 's/chr//' $1 | awk '{OFS="\t"; if (!/^#/){print $1,$2-1,$2,$4"/"$5,"+"}}'

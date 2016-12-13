#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 11/2016
# Purpose: Determine the size of a genome in bp

# Takes an input genome .fasta as a positional argument

sed -e '/^>/d' "$1"| wc -m
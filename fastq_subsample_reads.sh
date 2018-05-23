#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 5/2018
# Purpose: Randomly subsample single-end reads from pooled fastq, based on some stuff from stackoverflow about resevoir sampling.

# Takes two positional arguments, 1 is filename 2 is reads to sample. Outputs to stdout

cat $1 | \
awk '{ printf("%s",$0); n++; if(n%4==0) {printf("\n");} else { printf("\t");} }' | \
awk -v k=$2 'BEGIN{srand(systime() + PROCINFO["pid"]);}{s=x++<k?x-1:int(rand()*x);if(s<k)R[s]=$0}END{for(i in R)print R[i]}' | \
awk -F"\t" '{print $1"\n"$2"\n"$3"\n"$4}'


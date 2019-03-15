#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 3/2018
# Purpose: Get alignments from a sam file that have mismatches

grep -v 'NM:i:0' '$1'

#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 11/2017
# Purpose: grep lines from a bed file to an output bed file (subset the bed)
# Pass through the file to run as a positional variable

filename=$(basename "$2")
grep "$1" "$2" > "${filename%.bed}_${1}.bed"

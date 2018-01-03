#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 12/2017
# Purpose: Strips garbage from .fasta headers, edit the script as needed.

sed 's/|.*$//' "$1" > "${1%.fasta}.fixed_ids.fasta"

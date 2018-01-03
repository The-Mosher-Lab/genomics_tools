#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 12/2017
# Purpose: Convert fasta RNA sequences to DNA with sed

sed '/^[^>]/ y/uU/tT/' "$1"

#!/usr/bin/env bash

# Author: Jeffrey Grover
# Created: 11/2016
# Purpose: Determine the size of a genome in bp

sed -e '/^>/d' "$1"| wc -m
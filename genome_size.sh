#!/usr/bin/env bash

# Author: Jeffrey Grover, groverj3@gmail.com
# Purpose: Determine the size of a genome in bp

sed -e '/^>/d' "$1"| wc -m
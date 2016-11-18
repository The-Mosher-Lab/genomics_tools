#!/usr/bin/env bash

# Determine the size of a genome in bp

sed -e '/^>/d' "$1"| wc -m
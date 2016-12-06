#!/usr/bin/env Rscript

# Author: Jeffrey Grover
# Purpose: Create small RNA size distribution line plots from input files with two columns (counts), (length)
# Modified to output data normalized to abundance of 21 nt sRNAs
# Run on BASH command line, use 'find . -name "(p)" -exec "./size_profiles.R" {} \;' to batch process

library(ggplot2)

args = commandArgs(trailingOnly = TRUE)
input_file <- args[1]
readlengths <- read.table(input_file)

readlengths["21-normalized"] <- readlengths$V1/readlengths$V1[3] # Creates a new column normalized to 21 nt RNAs

ggplot(data = readlengths, aes(x = V2, y = `21-normalized`)) +
  geom_line(size = 2, color = "red") +
  theme(plot.title = element_text(size = 30)) + # Change axis titles
  ylab("Normalized Reads") + # \n adds a new line, increases distance between label and axis
  xlab("Length (nt)") +
  scale_x_continuous(breaks = 19:27, labels = 19:27) +
  theme(axis.text = element_text(size = 22)) + # Changes axis labels
  theme(axis.title = element_text(size = 25)) + # Change axis titles
  theme(axis.title.y = element_text(margin = margin(0, 15, 0, 0))) + # Changes label distance to axis 
  theme(axis.title.x = element_text(margin = margin(15, 0, 0, 0)))

# Saves output to .png based on input filename without .txt extension

ggsave(filename = paste(sub("\\.txt$", "", input_file), ".21_normalized.png", sep = ""), width = 7.5, height = 5) 

if(file.exists("Rplots.pdf")) file.remove("Rplots.pdf") # Removes unneeded Rplots.pdf that I can't suppress for some reason

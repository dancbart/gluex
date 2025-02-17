#!/bin/bash

env

time /w/halld-scshelf2101/home/dbarton/gluex/hd_utilities/FlattenForFSRoot/flatten \
                              -in INFILE \
                              -out OUTFILE \
                              -mctag 0_100000000_100001 \
                              -chi2 50 \
                              -combos 1 \
                              -numUnusedTracks 1 \
                              -numUnusedNeutrals 1 \
                              -addPID 1 \

# possibly change -in to -input
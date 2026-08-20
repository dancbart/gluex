#!/bin/bash

env

time /work/halld/home/dbarton/software/hd_utilities/FlattenForFSRoot/flatten \
                              -in INFILE \
                              -out OUTFILE \
                              -usePolarization 1 \
                              -dirc 1 \
                              -mctag 0_100000000_1100 \
                              -chi2 50 \
                              -combos 1 \
			                  -numUnusedTracks 1 \
                              -numUnusedNeutrals 1 \
                              -addPID 1 \

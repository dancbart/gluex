#!/bin/bash

env

time /home/dbart013/work/software/hd_utilities/FlattenForFSRoot/flatten \
                              -in INFILE \
                              -out OUTFILE \
                              -mctag 0_100000000_1100 \
                              -chi2 50 \
                              -usePolarization 1 \
			      -combos 1 \
                              -numUnusedTracks 1 \
                              -numUnusedNeutrals 1 \
                              -addPID 1 \

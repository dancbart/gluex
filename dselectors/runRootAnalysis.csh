#!/bin/tcsh

swif2 create -workflow  dselector_2017-01_ver22_batch02_MC_3body
python launch.py jobs_analysis_S18.config 30274 31057
#python launch.py jobs_analysis_F18.config 50685 51768
swif2 run -workflow  dselector_2017-01_ver22_batch02_MC_3body

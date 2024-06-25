#!/bin/tcsh

swif2 create -workflow  dselector_2017-01_ver22_batch01_MC_pipkmks
python launch.py jobs_analysis_S17.config 30274 31057
swif2 run -workflow  dselector_2017-01_ver22_batch01_MC_pipkmks

#!/bin/tcsh

swif2 create -workflow  dselector_2017-01_ver22_batch01_MC_pipkmks
python runDSelectorSWIF2_launch.py runDSelectorSWIF2_S17.config 30274 31057 #the original GlueX Python file is 'launch.py' and can be found elsewhere, e.g. in the GlueX GitHub repository.  It should be identical to this Python file.  Renamed for convenience.
swif2 run -workflow  dselector_2017-01_ver22_batch01_MC_pipkmks

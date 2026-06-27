#!/usr/bin/python3

import os
from subprocess import call
from datetime import datetime

#====================================================================================
# CONFIGURATION
#====================================================================================

workflow      = "MC_pipkslamb_2020-01_phaseSpace_spring2020"
timestamp     = datetime.today().strftime("%Y%m%d_%H%M%S")

configFile    = "/work/halld/home/dbarton/gluex/KShortPipLambda_MC/config_files/MC_genAmp2.config"

# Spring 2018
# runRangeLow   = 40856
# runRangeHigh  = 42559

# Fall 2018
# runRangeLow   = 50685
# runRangeHigh  = 51768

# Spring 2020
runRangeLow   = 71350
runRangeHigh  = 73266

# numEvents   = 1000    # per run (production)
numEvents   = 40000000    # per run (production)
batchMode     = 2

# logBaseDir    = "/farm_out/dbarton"

#====================================================================================
# SUBMISSION
#====================================================================================

# Resolve $MCWRAPPER_CENTRAL from the environment
mcwrapper_central = os.environ.get("MCWRAPPER_CENTRAL", "")
if not mcwrapper_central:
    print("ERROR: $MCWRAPPER_CENTRAL is not set. Are you inside the container?")
    exit(1)

mcWrapper = os.path.join(mcwrapper_central, "gluex_MC.py")

print("=" * 60)
print("Workflow         : %s" % workflow)
print("Config           : %s" % configFile)
print("Run range        : %d - %d" % (runRangeLow, runRangeHigh))
print("Events           : {:,} per run".format(numEvents))
print("Timestamp        : %s" % timestamp)
print("MCWRAPPER_CENTRAL: %s" % mcwrapper_central)
print("=" * 60)

# Create the swif2 workflow before submitting jobs
print("Creating workflow: %s" % workflow)
call("swif2 create %s" % workflow, shell=True)
print("")

cmd = (
    "{mcWrapper} {config} {runLow}-{runHigh} {nEvents} batch={batch}"
).format(
    mcWrapper = mcWrapper,
    config    = configFile,
    runLow    = runRangeLow,
    runHigh   = runRangeHigh,
    nEvents   = numEvents,
    batch     = batchMode,
)

print("Submitting run range %d-%d" % (runRangeLow, runRangeHigh))
print("  CMD: %s" % cmd)
call(cmd, shell=True)

print("")
print("=" * 60)
print("Done. Workflow: %s" % workflow)
print("=" * 60)

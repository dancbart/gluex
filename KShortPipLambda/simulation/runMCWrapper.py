#!/usr/bin/python3

import os
from subprocess import call
from datetime import datetime

#====================================================================================
# CONFIGURATION
#====================================================================================

configFile    = "/work/halld/home/dbarton/gluex/KShortPipLambda/simulation/config_files/MC_genAmp2.config"

# Spring 2018
# runRangeLow   = 40856
# runRangeHigh  = 42559
# numEvents   = 4000000000


# Fall 2018
# runRangeLow   = 50685
# runRangeHigh  = 51768
# numEvents   = 2600000000


# # Spring 2020
runRangeLow   = 71350
runRangeHigh  = 73266
numEvents   = 8000000000

batchMode = 2

# Read workflow name from config file
workflow = ""
with open(configFile) as f:
    for line in f:
        line = line.strip()
        if line.startswith("WORKFLOW_NAME"):
            workflow = line.split("=")[1].strip()
            break

if not workflow:
    print("ERROR: WORKFLOW_NAME not found in config file")
    exit(1)
    
# timestamp used in output folder naming
timestamp     = datetime.today().strftime("%Y%m%d_%H%M%S")
logBaseDir    = "/farm_out/dbarton"
logOutputDir = os.path.join(logBaseDir, "%s_%s" % (workflow, timestamp))
os.makedirs(logOutputDir, exist_ok=True)

#====================================================================================
# SUBMISSION
#====================================================================================

# USE IFARM'S MCWRAPPER:
# Resolve $MCWRAPPER_CENTRAL from the environment
mcwrapper_central = os.environ.get("MCWRAPPER_CENTRAL", "")
if not mcwrapper_central:
    print("ERROR: $MCWRAPPER_CENTRAL is not set. Have you sourced the GlueX environment'gxenv'?")
    exit(1)

mcWrapper = os.path.join(mcwrapper_central, "gluex_MC.py")

# ALTERNATE: USE LOCAL MCWRAPPER (hard-coded path)
# os.environ["MCWRAPPER_CENTRAL"] = "/work/halld/home/dbarton/software/gluex_MCwrapper"
# mcWrapper = "/work/halld/home/dbarton/software/gluex_MCwrapper/gluex_MC.py"

print("=" * 60)
print("Workflow         : %s" % workflow)
print("Config           : %s" % configFile)
print("Run range        : %d - %d" % (runRangeLow, runRangeHigh))
print("Events           : {:,} per run".format(numEvents))
print("Timestamp        : %s" % timestamp)
print("MCWRAPPER_CENTRAL: %s" % mcwrapper_central)
print("Log output dir   : %s" % logOutputDir)
print("=" * 60)

# Create the swif2 workflow before submitting jobs
print("Creating workflow: %s" % workflow)
call("swif2 create %s" % workflow, shell=True)
print("")

cmd = (
    "{mcWrapper} {config} {runLow}-{runHigh} {nEvents} batch={batch} logdir={logdir}"
).format(
    mcWrapper = mcWrapper,
    config    = configFile,
    runLow    = runRangeLow,
    runHigh   = runRangeHigh,
    nEvents   = numEvents,
    batch     = batchMode,
    logdir    = logOutputDir,
)

print("Submitting run range %d-%d" % (runRangeLow, runRangeHigh))
print("  CMD: %s" % cmd)
call(cmd, shell=True)

print("")
print("=" * 60)
print("Done. Workflow: %s" % workflow)
print("=" * 60)

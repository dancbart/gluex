#!/usr/bin/python3

import os
from subprocess import call
from datetime import datetime

workflow      = "FIT_pipkslamb_TwoPiAngles_500Mx3_MC"
timestamp     = datetime.today().strftime("%Y%m%d_%H%M%S")  # e.g. 20260601_143022

baseDir       = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/"
outputDir     = os.path.join(baseDir, "fits", "%s_%s" % (workflow, timestamp))
# configFile    = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/config/fit_TwoPiAngles_allPol.cfg"
configFile    = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/config/fit_TwoPiAngles_allPol_bkg.cfg"
num_fits      = 5

account       = "halld"
partition     = "production"
disk_space    = 6
mem_requested = 1
time_limit    = 5
NCORES        = "1" # change to 4 (or higher?) if script uses multi-threading.

# Create farm_out subdirectory for this run
os.makedirs(outputDir, exist_ok=True)
# farmoutDir = "/farm_out/dbarton/%s_%s" % (workflow, timestamp)
farmoutDir = os.path.join(outputDir, "%s_%s" % (workflow, timestamp))
os.makedirs(farmoutDir, exist_ok=True)

for fitNumber in range(1, num_fits + 1):

    # --- Write a per-fit wrapper bash script ---
    jobName    = "%s_%s_fit%04d" % (workflow, timestamp, fitNumber)
    scriptPath = os.path.join(outputDir, "run_fit_%04d.sh" % fitNumber)
    logFile    = os.path.join(farmoutDir, "fit%04d_stdout.out" % fitNumber)
    errFile    = os.path.join(farmoutDir, "fit%04d_stderr.err" % fitNumber)

    with open(scriptPath, "w") as f:
        f.write("#!/bin/bash\n\n")
        f.write("echo \"=== Fit %d of %d ===\"\n" % (fitNumber, num_fits))
        f.write('echo "Start time: $(date +\'%Y-%m-%d %H:%M:%S\')"\n')
        f.write("echo \"\"\n\n")
        f.write("cd %s\n\n" % outputDir)
        f.write("/work/halld/home/dbarton/software/halld_sim/src/.Linux_Alma9-x86_64-gcc11.5.0/programs/AmplitudeAnalysis/fit/fit -r %d -c %s\n\n" % (fitNumber, configFile))
        f.write("echo \"\"\n")
        f.write('echo "End time:   $(date +\'%Y-%m-%d %H:%M:%S\')"\n')
        f.write("echo \"=== Fit %d complete ===\"\n" % fitNumber)

    os.chmod(scriptPath, 0o755)

    # --- Submit one job per fit, all under the same workflow ---
    cmd  = "swif2 add-job -workflow %s -account %s -partition %s" % (workflow, account, partition)
    cmd += " -name %s"      % jobName
    cmd += " -constraint el9"
    cmd += " -stdout %s"    % logFile
    cmd += " -stderr %s"    % errFile
    cmd += " -create -cores " + NCORES
    cmd += " -disk %dGB"    % int(disk_space)
    cmd += " -ram %dGB"     % int(mem_requested)
    cmd += " -time %dhours" % int(time_limit)
    cmd += " " + scriptPath

    print("Submitting: %s -> %s" % (jobName, scriptPath))
    call(cmd, shell=True, stdout=None)

print("\nDone. Submitted %d jobs under workflow: %s" % (num_fits, workflow))
print("Output directory: %s" % outputDir)
print("Logs:             /farm_out/dbarton/log_%s_fit*.log" % workflow)

# --- Start the workflow ---
run_cmd = "swif2 run %s" % workflow
print("\nStarting workflow: %s" % workflow)
call(run_cmd, shell=True, stdout=None)